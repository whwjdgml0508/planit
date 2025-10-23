"""
URL configuration for planit_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.http import HttpResponse
import json

def manifest_view(request):
    """PWA 매니페스트 파일 서빙"""
    try:
        import os
        manifest_path = os.path.join(settings.STATIC_ROOT, 'manifest.json')
        if not os.path.exists(manifest_path):
            # 개발 환경에서는 static 폴더에서 찾기
            manifest_path = os.path.join(settings.BASE_DIR, 'static', 'manifest.json')
        
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest_data = f.read()
        return HttpResponse(manifest_data, content_type='application/json')
    except FileNotFoundError:
        # 파일이 없으면 기본 매니페스트 반환
        default_manifest = {
            "name": "PlanIt",
            "short_name": "PlanIt",
            "start_url": "/",
            "display": "standalone",
            "background_color": "#ffffff",
            "theme_color": "#0d6efd"
        }
        return HttpResponse(json.dumps(default_manifest), content_type='application/json')

def sw_view(request):
    """서비스 워커 파일 서빙"""
    try:
        import os
        sw_path = os.path.join(settings.STATIC_ROOT, 'sw.js')
        if not os.path.exists(sw_path):
            # 개발 환경에서는 static 폴더에서 찾기
            sw_path = os.path.join(settings.BASE_DIR, 'static', 'sw.js')
        
        with open(sw_path, 'r', encoding='utf-8') as f:
            sw_data = f.read()
        return HttpResponse(sw_data, content_type='application/javascript')
    except FileNotFoundError:
        # 파일이 없으면 기본 서비스 워커 반환
        default_sw = """
        const CACHE_NAME = 'planit-v1';
        self.addEventListener('install', event => {
            console.log('Service Worker installed');
        });
        """
        return HttpResponse(default_sw, content_type='application/javascript')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('install/', TemplateView.as_view(template_name='install.html'), name='install'),
    path('manifest.json', manifest_view, name='manifest'),
    path('sw.js', sw_view, name='sw'),
    
    # API URLs (temporarily commented out)
    # path('api/v1/', include('api.urls')),
    # path('api/schema/', include('drf_spectacular.urls')),
    
    # Web URLs
    path('accounts/', include('accounts.urls')),
    path('timetable/', include('timetable.urls')),
    path('planner/', include('planner.urls')),
    path('community/', include('community.urls')),
]

# Static and media files serving
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
