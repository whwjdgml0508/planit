#!/usr/bin/env python3
import os
import sys
import django

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.development')
sys.path.append('/home/ubuntu/planit')
django.setup()

from django.contrib.auth import get_user_model

def main():
    User = get_user_model()
    
    print("=== PlanIt Admin 계정 생성 ===")
    
    # 현재 사용자 확인
    print("현재 사용자 목록:")
    for user in User.objects.all():
        print(f"- {user.username} (관리자: {user.is_superuser})")
    
    # admin 계정 생성/업데이트
    if User.objects.filter(username='admin').exists():
        print("admin 계정이 이미 존재합니다.")
        admin_user = User.objects.get(username='admin')
        admin_user.is_superuser = True
        admin_user.is_staff = True
        admin_user.save()
        print("admin 계정에 관리자 권한을 부여했습니다.")
    else:
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@planit.boramae.club',
            password='planit2024!',
            student_id='0000000',
            first_name='관리자',
            last_name='시스템'
        )
        print("새로운 admin 계정이 생성되었습니다!")
    
    # 결과 확인
    admin_user = User.objects.get(username='admin')
    print(f"Admin 계정 확인:")
    print(f"- 사용자명: {admin_user.username}")
    print(f"- 이메일: {admin_user.email}")
    print(f"- 관리자 권한: {admin_user.is_superuser}")
    print(f"- 스태프 권한: {admin_user.is_staff}")
    print("로그인 정보: admin / planit2024!")

if __name__ == '__main__':
    main()
