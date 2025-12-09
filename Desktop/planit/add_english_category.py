#!/usr/bin/env python
"""
영어상식 카테고리 추가 스크립트
"""
import os
import sys
import django

# Django 설정
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 환경에 따라 설정 선택
if os.path.exists('/home/ubuntu/planit'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.development')

django.setup()

from community.models import Category

def add_english_category():
    """영어상식 카테고리 추가"""
    try:
        # 영어상식 카테고리 생성 또는 업데이트
        category, created = Category.objects.update_or_create(
            slug='english',
            defaults={
                'name': '🌍 영어상식',
                'category_type': 'ENGLISH',
                'description': '영어 학습 팁, 토익/토플 정보, 영어 관련 자료를 공유합니다',
                'icon': 'fas fa-globe',
                'color': '#17a2b8',
                'order': 5,
                'is_active': True,
            }
        )
        
        if created:
            print(f"✅ 영어상식 카테고리 생성 완료!")
        else:
            print(f"🔄 영어상식 카테고리 업데이트 완료!")
        
        print(f"\n카테고리 정보:")
        print(f"  - 이름: {category.name}")
        print(f"  - 슬러그: {category.slug}")
        print(f"  - 타입: {category.get_category_type_display()}")
        print(f"  - 설명: {category.description}")
        print(f"  - 아이콘: {category.icon}")
        print(f"  - 색상: {category.color}")
        print(f"  - 정렬순서: {category.order}")
        
        # 전체 카테고리 목록 출력
        print(f"\n현재 활성화된 카테고리 목록:")
        for cat in Category.objects.filter(is_active=True).order_by('order'):
            print(f"  {cat.order}. {cat.name} ({cat.slug})")
        
        return True
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("영어상식 카테고리 추가")
    print("=" * 60)
    
    if add_english_category():
        print("\n✅ 작업 완료!")
    else:
        print("\n❌ 작업 실패")
