#!/usr/bin/env python
import os
import django

# Production Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.production')
django.setup()

from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

print("=== Production Admin 계정 확인 ===")

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
            print(f"✅ 비밀번호 '{pwd}'가 맞습니다!")
            password_found = True
            break
        else:
            print(f"❌ '{pwd}' - 틀림")
    
    if not password_found:
        print("⚠️ 테스트한 비밀번호들이 모두 틀렸습니다.")
        print("비밀번호를 재설정해야 할 수 있습니다.")
    
    # 인증 테스트
    print("\n인증 테스트:")
    if password_found:
        correct_password = None
        for pwd in test_passwords:
            if admin.check_password(pwd):
                correct_password = pwd
                break
        
        user = authenticate(username='admin', password=correct_password)
        if user:
            print(f"✅ authenticate 성공: {user.username}")
        else:
            print("❌ authenticate 실패")
    
except User.DoesNotExist:
    print("❌ Admin 계정이 존재하지 않습니다.")
    print("새로운 admin 계정을 생성해야 합니다.")

print("\n=== 전체 사용자 목록 ===")
users = User.objects.all()
for user in users:
    print(f"- {user.username} (슈퍼유저: {user.is_superuser}, 활성화: {user.is_active})")
