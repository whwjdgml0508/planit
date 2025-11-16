#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.production')
django.setup()

from community.models import Category

print("=== Category Status Check ===")
categories = Category.objects.all().order_by('order')
print(f"Total categories: {categories.count()}")

for cat in categories:
    print(f"- {cat.name} ({cat.slug}) - Active: {cat.is_active}")

print("\n=== Active Categories Only ===")
active_categories = Category.objects.filter(is_active=True).order_by('order')
print(f"Active categories: {active_categories.count()}")

for cat in active_categories:
    print(f"- {cat.name} ({cat.slug})")
