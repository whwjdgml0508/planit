"""
Production 서버에 필요한 카테고리들을 생성하는 스크립트
"""
import os
import sys
import django

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.development')
django.setup()

from community.models import Category

# 생성할 카테고리 목록
CATEGORIES = [
    {
        'name': '📚 학습 자료',
        'slug': 'study',
        'category_type': 'STUDY',
        'description': '학습 자료를 공유하는 게시판입니다.',
        'icon': 'fas fa-book',
        'color': '#28a745',
        'order': 1,
    },
    {
        'name': '📝 시험 정보',
        'slug': 'exam',
        'category_type': 'EXAM',
        'description': '시험 정보를 공유하는 게시판입니다.',
        'icon': 'fas fa-file-alt',
        'color': '#dc3545',
        'order': 2,
    },
    {
        'name': '🎓 강의 특성',
        'slug': 'lecture',
        'category_type': 'LECTURE',
        'description': '강의 특성 및 교수님 정보를 공유하는 게시판입니다.',
        'icon': 'fas fa-chalkboard-teacher',
        'color': '#6f42c1',
        'order': 3,
    },
    {
        'name': '💪 체력평가',
        'slug': 'fitness',
        'category_type': 'FITNESS',
        'description': '체력평가 팁을 공유하는 게시판입니다.',
        'icon': 'fas fa-running',
        'color': '#fd7e14',
        'order': 4,
    },
    {
        'name': '🌍 영어 상식',
        'slug': 'english',
        'category_type': 'ENGLISH',
        'description': '영어 상식을 공유하는 게시판입니다.',
        'icon': 'fas fa-globe',
        'color': '#17a2b8',
        'order': 5,
    },
    {
        'name': '💻 프로젝트',
        'slug': 'project',
        'category_type': 'PROJECT',
        'description': '프로젝트 관련 정보를 공유하는 게시판입니다.',
        'icon': 'fas fa-laptop-code',
        'color': '#20c997',
        'order': 6,
    },
    {
        'name': '❓ 질문답변',
        'slug': 'qna',
        'category_type': 'QNA',
        'description': '질문과 답변을 나누는 게시판입니다.',
        'icon': 'fas fa-question-circle',
        'color': '#6610f2',
        'order': 7,
    },
    {
        'name': '💬 자유게시판',
        'slug': 'free',
        'category_type': 'FREE',
        'description': '자유롭게 이야기하는 게시판입니다.',
        'icon': 'fas fa-comments',
        'color': '#007bff',
        'order': 8,
    },
    {
        'name': '📢 공지사항',
        'slug': 'notice',
        'category_type': 'NOTICE',
        'description': '공지사항 게시판입니다.',
        'icon': 'fas fa-bullhorn',
        'color': '#ffc107',
        'order': 0,
    },
]

def create_categories():
    """카테고리 생성"""
    created_count = 0
    updated_count = 0
    
    for cat_data in CATEGORIES:
        category, created = Category.objects.update_or_create(
            slug=cat_data['slug'],
            defaults={
                'name': cat_data['name'],
                'category_type': cat_data['category_type'],
                'description': cat_data['description'],
                'icon': cat_data['icon'],
                'color': cat_data['color'],
                'order': cat_data['order'],
                'is_active': True,
            }
        )
        
        if created:
            print(f"✅ 생성됨: {category.name} (slug: {category.slug})")
            created_count += 1
        else:
            print(f"🔄 업데이트됨: {category.name} (slug: {category.slug})")
            updated_count += 1
    
    print(f"\n총 {created_count}개 생성, {updated_count}개 업데이트됨")
    
    # 현재 카테고리 목록 출력
    print("\n현재 카테고리 목록:")
    for cat in Category.objects.filter(is_active=True).order_by('order'):
        print(f"  - {cat.name} (slug: {cat.slug})")

if __name__ == '__main__':
    print("카테고리 생성/업데이트 시작...\n")
    create_categories()
    print("\n완료!")
