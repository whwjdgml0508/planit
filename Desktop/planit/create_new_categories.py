#!/usr/bin/env python
"""
새로운 커뮤니티 카테고리 생성 스크립트
"""
import os
import sys
import django

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.development')
django.setup()

from community.models import Category

def create_new_categories():
    """새로운 카테고리들을 생성합니다."""
    
    new_categories = [
        {
            'name': '학습 자료 공유',
            'slug': 'study-share',
            'category_type': 'STUDY_SHARE',
            'description': '학습에 도움이 되는 자료를 공유하는 공간입니다.',
            'icon': 'fas fa-share-alt',
            'color': '#28a745',
            'order': 1
        },
        {
            'name': '체력 평가 팁',
            'slug': 'fitness-tips',
            'category_type': 'FITNESS_TIPS',
            'description': '체력 평가 준비와 관련된 팁을 공유하는 공간입니다.',
            'icon': 'fas fa-dumbbell',
            'color': '#dc3545',
            'order': 2
        },
        {
            'name': '학교 생활 팁',
            'slug': 'school-tips',
            'category_type': 'SCHOOL_TIPS',
            'description': '학교 생활에 도움이 되는 다양한 팁을 공유하는 공간입니다.',
            'icon': 'fas fa-school',
            'color': '#17a2b8',
            'order': 3
        },
        {
            'name': '직접 입력',
            'slug': 'custom',
            'category_type': 'CUSTOM',
            'description': '사용자가 직접 주제를 정해서 작성하는 공간입니다.',
            'icon': 'fas fa-edit',
            'color': '#6f42c1',
            'order': 4
        }
    ]
    
    created_count = 0
    
    for category_data in new_categories:
        category, created = Category.objects.get_or_create(
            slug=category_data['slug'],
            defaults=category_data
        )
        
        if created:
            print(f"[SUCCESS] 새 카테고리 생성: {category.name}")
            created_count += 1
        else:
            print(f"[INFO] 이미 존재하는 카테고리: {category.name}")
    
    print(f"\n[COMPLETE] 총 {created_count}개의 새로운 카테고리가 생성되었습니다!")
    
    # 모든 카테고리 목록 출력
    print("\n[LIST] 현재 활성화된 카테고리 목록:")
    categories = Category.objects.filter(is_active=True).order_by('order', 'name')
    for i, category in enumerate(categories, 1):
        print(f"{i:2d}. {category.name} ({category.get_category_type_display()})")

if __name__ == '__main__':
    try:
        create_new_categories()
    except Exception as e:
        print(f"[ERROR] 오류 발생: {e}")
        sys.exit(1)
