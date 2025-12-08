#!/usr/bin/env python
import os
import django

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.development')
django.setup()

from django.contrib.auth import authenticate, login
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware

# 로그인 테스트
def test_login():
    print("=== 로그인 테스트 ===")
    
    # 1. authenticate 함수 테스트
    user = authenticate(username='admin', password='admin123')
    if user:
        print(f"✅ authenticate 성공: {user.username}")
        print(f"   - 활성화: {user.is_active}")
        print(f"   - 슈퍼유저: {user.is_superuser}")
    else:
        print("❌ authenticate 실패")
        return
    
    # 2. 실제 로그인 시뮬레이션
    factory = RequestFactory()
    request = factory.post('/accounts/login/')
    
    # 세션 미들웨어 추가
    middleware = SessionMiddleware(lambda x: None)
    middleware.process_request(request)
    request.session.save()
    
    # 인증 미들웨어 추가
    auth_middleware = AuthenticationMiddleware(lambda x: None)
    auth_middleware.process_request(request)
    
    # 로그인 시도
    login(request, user)
    
    if request.user.is_authenticated:
        print("✅ 로그인 시뮬레이션 성공")
        print(f"   - 로그인된 사용자: {request.user.username}")
    else:
        print("❌ 로그인 시뮬레이션 실패")

if __name__ == '__main__':
    test_login()
