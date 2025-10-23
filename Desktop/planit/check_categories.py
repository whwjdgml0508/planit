#!/usr/bin/env python
import os
import django

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.development')
django.setup()

from community.models import Category
from django.utils.text import slugify

print("현재 카테고리들:")
for cat in Category.objects.all():
    print(f'ID: {cat.id}, Name: {cat.name}, Slug: "{cat.slug}"')

print("\n슬러그 테스트:")
test_names = ['학습 자료', '시험 정보', '강의 특성']
for name in test_names:
    print(f'{name} -> {slugify(name)}')

print(f"\n총 카테고리 수: {Category.objects.count()}")
