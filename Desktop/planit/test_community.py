#!/usr/bin/env python
import os
import django

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.development')
django.setup()

from community.models import Category
from community.views import CommunityView
from django.test import RequestFactory
from django.contrib.auth import get_user_model

User = get_user_model()

# 기존 admin 사용자 사용
try:
    user = User.objects.get(username='admin')
except User.DoesNotExist:
    print("admin 사용자가 없습니다. 먼저 관리자 계정을 생성해주세요.")
    exit(1)

print("=== 커뮤니티 카테고리 테스트 ===")
print(f"총 카테고리 수: {Category.objects.count()}")
print("\n활성 카테고리 목록:")
for category in Category.objects.filter(is_active=True).order_by('order'):
    print(f"- {category.name} ({category.category_type}) - {category.slug}")
    print(f"  설명: {category.description}")
    print(f"  아이콘: {category.icon}, 색상: {category.color}")
    print()

# 뷰 테스트
print("=== 커뮤니티 뷰 테스트 ===")
factory = RequestFactory()
request = factory.get('/community/')
request.user = user

view = CommunityView()
view.request = request
context = view.get_context_data()

print(f"뷰에서 전달되는 카테고리 수: {context['categories'].count()}")
print("뷰에서 전달되는 카테고리들:")
for category in context['categories']:
    print(f"- {category.name} (게시글 수: {category.post_count})")
