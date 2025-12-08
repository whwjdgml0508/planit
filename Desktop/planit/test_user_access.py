#!/usr/bin/env python
import os
import sys
import django

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.development')
django.setup()

from django.contrib.auth.models import User
from accounts.models import User as CustomUser
from community.models import Category
from django.db.models import Q

def test_user_access():
    print("=== 사용자 접근 테스트 ===\n")
    
    # 일반 사용자 테스트
    try:
        user = CustomUser.objects.get(username='공군')
        print(f"사용자: {user.username}")
        print(f"학과: {user.department}")
        print(f"스태프: {user.is_staff}")
        print(f"슈퍼유저: {user.is_superuser}")
        
        # 커뮤니티 카테고리 접근 테스트
        print("\n=== 커뮤니티 카테고리 접근 테스트 ===")
        categories = Category.objects.filter(is_active=True)
        print(f"전체 활성 카테고리 수: {categories.count()}")
        
        if not user.is_staff:
            accessible_categories = categories.filter(
                Q(department_restricted=False) |
                Q(allowed_departments__icontains=user.department)
            )
            print(f"일반 사용자 접근 가능 카테고리 수: {accessible_categories.count()}")
            
            for cat in accessible_categories:
                print(f"  - {cat.name} (학과제한: {cat.department_restricted})")
        
        # 각 앱별 모델 접근 테스트
        print("\n=== 각 앱별 데이터 접근 테스트 ===")
        
        # Planner 앱
        from planner.models import Task
        user_tasks = Task.objects.filter(user=user)
        print(f"Planner - 사용자 과제 수: {user_tasks.count()}")
        
        # Timetable 앱
        from timetable.models import Subject
        user_subjects = Subject.objects.filter(user=user)
        print(f"Timetable - 사용자 과목 수: {user_subjects.count()}")
        
        # Community 앱
        from community.models import Post
        user_posts = Post.objects.filter(author=user)
        print(f"Community - 사용자 게시글 수: {user_posts.count()}")
        
    except Exception as e:
        print(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_user_access()
