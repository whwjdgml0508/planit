#!/usr/bin/env python
import os
import sys
import django

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.development')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from accounts.models import User as CustomUser

def check_user_permissions():
    print("=== 사용자 권한 분석 ===\n")
    
    # 모든 사용자 조회
    users = CustomUser.objects.all()
    print(f"총 사용자 수: {users.count()}\n")
    
    for user in users:
        print(f"사용자: {user.username}")
        print(f"  - 이메일: {user.email}")
        print(f"  - 학번: {getattr(user, 'student_id', 'N/A')}")
        print(f"  - 학과: {getattr(user, 'department', 'N/A')}")
        print(f"  - 활성화: {user.is_active}")
        print(f"  - 스태프: {user.is_staff}")
        print(f"  - 슈퍼유저: {user.is_superuser}")
        print(f"  - 마지막 로그인: {user.last_login}")
        
        # 그룹 확인
        groups = user.groups.all()
        print(f"  - 그룹: {[g.name for g in groups]}")
        
        # 권한 확인
        permissions = user.user_permissions.all()
        print(f"  - 직접 권한: {[p.codename for p in permissions]}")
        
        # 모든 권한 (그룹 포함)
        all_permissions = user.get_all_permissions()
        print(f"  - 모든 권한 수: {len(all_permissions)}")
        
        print("-" * 50)
    
    # 그룹 정보
    print("\n=== 그룹 정보 ===")
    groups = Group.objects.all()
    for group in groups:
        print(f"그룹: {group.name}")
        print(f"  - 권한: {[p.codename for p in group.permissions.all()]}")
        print(f"  - 멤버: {[u.username for u in group.user_set.all()]}")
        print("-" * 30)

if __name__ == "__main__":
    check_user_permissions()
