#!/usr/bin/env python
"""
영어 상식 카테고리 이름 수정 스크립트
"영어 상식" -> "영어상식" (공백 제거)
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

def fix_english_category():
    """영어 상식 카테고리 이름 수정"""
    try:
        # "영어 상식" 또는 "🌍 영어 상식" 카테고리 찾기
        categories = Category.objects.filter(category_type='ENGLISH')
        
        if not categories.exists():
            print("❌ 영어 상식 카테고리를 찾을 수 없습니다.")
            return False
        
        for category in categories:
            old_name = category.name
            # 공백 제거
            if '영어 상식' in category.name:
                category.name = category.name.replace('영어 상식', '영어상식')
                category.save()
                print(f"✅ 카테고리 이름 수정: '{old_name}' -> '{category.name}'")
            else:
                print(f"ℹ️ 이미 올바른 이름: '{category.name}'")
        
        return True
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("=" * 50)
    print("영어 상식 카테고리 이름 수정")
    print("=" * 50)
    
    if fix_english_category():
        print("\n✅ 카테고리 이름 수정 완료!")
    else:
        print("\n❌ 카테고리 이름 수정 실패")
