#!/usr/bin/env python
import os
import django

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.development')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

try:
    admin = User.objects.get(username='admin')
    print("Admin 계정 정보:")
    print(f"- 사용자명: {admin.username}")
    print(f"- 이메일: {admin.email}")
    print(f"- 활성화: {admin.is_active}")
    print(f"- 슈퍼유저: {admin.is_superuser}")
    print(f"- 스태프: {admin.is_staff}")
    print(f"- 학번: {getattr(admin, 'student_id', 'N/A')}")
    print(f"- 마지막 로그인: {admin.last_login}")
    print(f"- 가입일: {admin.date_joined}")
    
    # 비밀번호 테스트
    test_passwords = ['admin', 'admin123', 'password', '1234', 'planit123']
    print("\n비밀번호 테스트:")
    password_found = False
    for pwd in test_passwords:
        if admin.check_password(pwd):
            print(f"OK - 비밀번호 '{pwd}'가 맞습니다!")
            password_found = True
            break
    
    if not password_found:
        print("ERROR - 테스트한 비밀번호들이 모두 틀렸습니다.")
        
except User.DoesNotExist:
    print("Admin 계정이 존재하지 않습니다.")
