#!/usr/bin/env python
"""
Simple admin creation script for PlanIt
서버에 업로드해서 실행할 수 있는 간단한 admin 계정 생성 스크립트
"""

import os
import sys
import django

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.production')
django.setup()

from django.contrib.auth import get_user_model

def create_admin_user():
    User = get_user_model()
    
    print("=== PlanIt Admin 계정 생성 ===")
    
    # 현재 사용자 목록 확인
    print("\n현재 등록된 사용자:")
    for user in User.objects.all():
        print(f"- {user.username} (관리자: {user.is_superuser})")
    print(f"총 {User.objects.count()}명의 사용자가 등록되어 있습니다.\n")
    
    # admin 계정 확인/생성
    if User.objects.filter(username='admin').exists():
        print("admin 계정이 이미 존재합니다.")
        admin_user = User.objects.get(username='admin')
        
        # 관리자 권한 확인/부여
        if not admin_user.is_superuser:
            admin_user.is_superuser = True
            admin_user.is_staff = True
            admin_user.save()
            print("기존 admin 계정에 관리자 권한을 부여했습니다.")
        else:
            print("admin 계정은 이미 관리자 권한을 가지고 있습니다.")
    else:
        # 새로운 admin 계정 생성
        try:
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@planit.boramae.club',
                password='planit2024!',
                student_id='0000000',  # 커스텀 User 모델 필수 필드
                first_name='관리자',
                last_name='시스템'
            )
            print("✅ 새로운 admin 계정이 생성되었습니다!")
            print("📋 로그인 정보:")
            print("   - 사용자명: admin")
            print("   - 비밀번호: planit2024!")
            print("   - 이메일: admin@planit.boramae.club")
        except Exception as e:
            print(f"❌ admin 계정 생성 실패: {e}")
            return False
    
    # 최종 확인
    try:
        admin_user = User.objects.get(username='admin')
        print(f"\n✅ Admin 계정 확인:")
        print(f"   - 사용자명: {admin_user.username}")
        print(f"   - 이메일: {admin_user.email}")
        print(f"   - 관리자 권한: {admin_user.is_superuser}")
        print(f"   - 스태프 권한: {admin_user.is_staff}")
        print(f"   - 학번: {admin_user.student_id}")
        print(f"\n🌐 관리자 페이지: http://planit.boramae.club/admin/")
        return True
    except User.DoesNotExist:
        print("❌ admin 계정을 찾을 수 없습니다.")
        return False

if __name__ == '__main__':
    success = create_admin_user()
    sys.exit(0 if success else 1)
