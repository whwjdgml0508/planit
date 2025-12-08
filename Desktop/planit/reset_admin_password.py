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
    
    # 새 비밀번호 설정
    new_password = 'admin123'
    admin.set_password(new_password)
    admin.save()
    
    print(f"Admin 계정 비밀번호가 '{new_password}'로 재설정되었습니다.")
    print("이제 다음 정보로 로그인할 수 있습니다:")
    print(f"- 사용자명: {admin.username}")
    print(f"- 비밀번호: {new_password}")
    
    # 비밀번호 확인
    if admin.check_password(new_password):
        print("비밀번호 재설정이 성공적으로 완료되었습니다!")
    else:
        print("ERROR: 비밀번호 재설정에 실패했습니다.")
        
except User.DoesNotExist:
    print("Admin 계정이 존재하지 않습니다.")
    print("새로운 admin 계정을 생성합니다...")
    
    # 새 admin 계정 생성
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )
    print("새 admin 계정이 생성되었습니다:")
    print("- 사용자명: admin")
    print("- 비밀번호: admin123")
