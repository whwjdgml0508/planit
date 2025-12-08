#!/usr/bin/env python
import os
import sys
import django

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.development')
django.setup()

from accounts.models import User as CustomUser
from community.models import Category

def check_error_details():
    print("=== 오류 상세 분석 ===\n")
    
    # 모든 사용자 조회
    users = CustomUser.objects.all()
    for user in users:
        print(f"사용자 ID: {user.id}")
        print(f"사용자명: {repr(user.username)}")  # repr로 정확한 문자열 확인
        print(f"이메일: {user.email}")
        print(f"학과: {user.department}")
        print(f"스태프: {user.is_staff}")
        print(f"슈퍼유저: {user.is_superuser}")
        print("-" * 40)
    
    # 일반 사용자 (admin이 아닌) 선택
    regular_user = users.filter(is_superuser=False).first()
    if regular_user:
        print(f"\n=== 일반 사용자 테스트: {regular_user.username} ===")
        
        # 커뮤니티 카테고리 확인
        categories = Category.objects.filter(is_active=True)
        print(f"전체 카테고리 수: {categories.count()}")
        
        for cat in categories:
            print(f"카테고리: {cat.name}")
            print(f"  - 학과 제한: {cat.department_restricted}")
            print(f"  - 허용 학과: {cat.allowed_departments}")
            
            # 사용자 접근 가능 여부 확인
            can_access = False
            if not cat.department_restricted:
                can_access = True
            elif regular_user.department in cat.allowed_departments:
                can_access = True
            
            print(f"  - 사용자 접근 가능: {can_access}")
            print()

if __name__ == "__main__":
    check_error_details()
