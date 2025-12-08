#!/usr/bin/env python
"""
회원가입 상태 실시간 확인 스크립트
"""
import os
import django

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.development')
django.setup()

from accounts.models import User
from django.db import connection

def check_registration_status():
    """회원가입 관련 상태 확인"""
    
    print("=== PlanIt 회원가입 상태 확인 ===\n")
    
    # 1. 데이터베이스 연결 확인
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("[OK] 데이터베이스 연결: 정상")
    except Exception as e:
        print(f"[ERROR] 데이터베이스 연결 오류: {e}")
        return
    
    # 2. User 모델 확인
    try:
        total_users = User.objects.count()
        print(f"[OK] 총 사용자 수: {total_users}명")
        
        # 최근 생성된 사용자 5명
        recent_users = User.objects.order_by('-date_joined')[:5]
        if recent_users:
            print("[OK] 최근 가입 사용자:")
            for user in recent_users:
                print(f"  - {user.username} ({user.student_id}) - {user.date_joined.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print("- 가입된 사용자가 없습니다.")
            
    except Exception as e:
        print(f"[ERROR] User 모델 오류: {e}")
    
    # 3. 회원가입 폼 필드 확인
    try:
        from accounts.forms import CustomUserCreationForm
        form = CustomUserCreationForm()
        print(f"[OK] 회원가입 폼 필드 수: {len(form.fields)}개")
        print("[OK] 필수 필드:")
        for field_name, field in form.fields.items():
            required = "필수" if field.required else "선택"
            print(f"  - {field_name}: {field.label} ({required})")
    except Exception as e:
        print(f"[ERROR] 폼 확인 오류: {e}")
    
    # 4. URL 패턴 확인
    try:
        from django.urls import reverse
        register_url = reverse('accounts:register')
        print(f"[OK] 회원가입 URL: {register_url}")
    except Exception as e:
        print(f"[ERROR] URL 패턴 오류: {e}")
    
    # 5. 서버 설정 확인
    from django.conf import settings
    print(f"[OK] DEBUG 모드: {settings.DEBUG}")
    print(f"[OK] ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    
    print("\n=== 브라우저 테스트 가이드 ===")
    print("1. 브라우저에서 http://127.0.0.1:8000/accounts/register/ 접속")
    print("2. F12로 개발자 도구 열기")
    print("3. Network 탭에서 HTTP 요청 모니터링")
    print("4. 회원가입 시도 후 실제 응답 코드 확인")
    print("5. Console 탭에서 JavaScript 오류 확인")

if __name__ == '__main__':
    check_registration_status()
