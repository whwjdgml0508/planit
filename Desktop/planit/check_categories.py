#!/usr/bin/env python
import os
import django

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.production')
django.setup()

from community.models import Category

print("=== 카테고리 데이터 확인 ===")
print(f"총 카테고리 수: {Category.objects.count()}")
print(f"활성 카테고리 수: {Category.objects.filter(is_active=True).count()}")

print("\n현재 카테고리들:")
for cat in Category.objects.all():
    print(f'- ID: {cat.id}, Name: {cat.name}, Active: {cat.is_active}, Icon: {cat.icon}')

if Category.objects.count() == 0:
    print("\n카테고리가 없습니다. 기본 카테고리를 생성합니다...")
    
    categories_data = [
        {
            'name': '📚 학습자료',
            'slug': 'study-materials',
            'category_type': 'STUDY',
            'description': '강의 자료, 요약 노트, 참고 자료 등을 공유하는 공간입니다.',
            'icon': '📚',
            'color': '#3498db',
            'order': 1,
            'is_active': True,
            'department_restricted': False,
        },
        {
            'name': '📝 시험정보',
            'slug': 'exam-info',
            'category_type': 'EXAM',
            'description': '시험 일정, 출제 경향, 시험 후기 등을 공유하는 공간입니다.',
            'icon': '📝',
            'color': '#e74c3c',
            'order': 2,
            'is_active': True,
            'department_restricted': False,
        },
        {
            'name': '💪 체력평가',
            'slug': 'fitness',
            'category_type': 'FITNESS',
            'description': '체력평가 정보, 운동 팁, 훈련 방법 등을 공유하는 공간입니다.',
            'icon': '💪',
            'color': '#2ecc71',
            'order': 3,
            'is_active': True,
            'department_restricted': False,
        },
        {
            'name': '💬 자유게시판',
            'slug': 'free-board',
            'category_type': 'FREE',
            'description': '자유로운 소통과 정보 교환을 위한 공간입니다.',
            'icon': '💬',
            'color': '#9b59b6',
            'order': 4,
            'is_active': True,
            'department_restricted': False,
        },
        {
            'name': '📢 공지사항',
            'slug': 'notice',
            'category_type': 'NOTICE',
            'description': '중요한 공지사항과 안내사항을 게시하는 공간입니다.',
            'icon': '📢',
            'color': '#f39c12',
            'order': 0,
            'is_active': True,
            'department_restricted': False,
        }
    ]
    
    for cat_data in categories_data:
        category = Category.objects.create(**cat_data)
        print(f"생성됨: {category.name}")
    
    print(f"\n카테고리 생성 완료! 총 {Category.objects.count()}개")
else:
    print("\n카테고리가 이미 존재합니다.")
