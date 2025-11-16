#!/usr/bin/env python3
import os
import django

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.production')
django.setup()

from community.models import Category

def create_categories():
    categories_data = [
        {
            'name': '공지사항',
            'slug': 'notices',
            'category_type': 'NOTICE',
            'description': '중요한 공지사항을 전달하는 공간입니다',
            'icon': 'fas fa-bullhorn',
            'color': '#ffc107',
            'order': 0
        },
        {
            'name': '학습 자료',
            'slug': 'study-materials',
            'category_type': 'STUDY',
            'description': '강의 자료, 노트, 참고 자료 등을 공유하는 공간입니다',
            'icon': 'fas fa-book',
            'color': '#28a745',
            'order': 1
        },
        {
            'name': '시험 정보',
            'slug': 'exam-info',
            'category_type': 'EXAM',
            'description': '시험 일정, 출제 경향, 기출문제 등 시험 관련 정보를 공유합니다',
            'icon': 'fas fa-clipboard-check',
            'color': '#dc3545',
            'order': 2
        },
        {
            'name': '강의 특성',
            'slug': 'lecture-info',
            'category_type': 'LECTURE',
            'description': '교수님별 강의 특성, 수업 방식 등에 대한 정보를 나눕니다',
            'icon': 'fas fa-chalkboard-teacher',
            'color': '#6f42c1',
            'order': 3
        },
        {
            'name': '체력평가',
            'slug': 'fitness-test',
            'category_type': 'FITNESS',
            'description': '체력평가 준비 방법, 팁, 경험담을 공유합니다',
            'icon': 'fas fa-running',
            'color': '#fd7e14',
            'order': 4
        },
        {
            'name': '영어 상식',
            'slug': 'english-tips',
            'category_type': 'ENGLISH',
            'description': '영어 학습 팁, 토익/토플 정보, 영어 관련 자료를 공유합니다',
            'icon': 'fas fa-language',
            'color': '#20c997',
            'order': 5
        },
        {
            'name': '프로젝트',
            'slug': 'projects',
            'category_type': 'PROJECT',
            'description': '팀 프로젝트 모집, 포트폴리오 공유, 개발 관련 정보를 나눕니다',
            'icon': 'fas fa-code',
            'color': '#6610f2',
            'order': 6
        },
        {
            'name': '질문답변',
            'slug': 'qna',
            'category_type': 'QNA',
            'description': '궁금한 점을 질문하고 답변을 받는 공간입니다',
            'icon': 'fas fa-question-circle',
            'color': '#17a2b8',
            'order': 7
        },
        {
            'name': '자유게시판',
            'slug': 'free-board',
            'category_type': 'FREE',
            'description': '자유로운 주제로 이야기를 나누는 공간입니다',
            'icon': 'fas fa-comments',
            'color': '#007bff',
            'order': 8
        }
    ]

    created_count = 0
    for category_data in categories_data:
        slug = category_data['slug']
        
        # 이미 존재하는 카테고리는 건너뛰기
        if Category.objects.filter(slug=slug).exists():
            print(f'카테고리 "{category_data["name"]}"는 이미 존재합니다.')
            continue
        
        category = Category.objects.create(
            name=category_data['name'],
            slug=slug,
            category_type=category_data['category_type'],
            description=category_data['description'],
            icon=category_data['icon'],
            color=category_data['color'],
            order=category_data['order'],
            is_active=True
        )
        
        created_count += 1
        print(f'카테고리 "{category.name}" 생성 완료')

    print(f'\n총 {created_count}개의 카테고리가 생성되었습니다.')
    print(f'현재 총 카테고리 수: {Category.objects.count()}')

if __name__ == '__main__':
    create_categories()
