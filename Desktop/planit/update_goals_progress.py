#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.production')
django.setup()

from planner.models import Goal

# 모든 목표의 progress를 0으로 초기화
count = Goal.objects.all().update(progress=0)
print(f'Updated {count} goals with progress=0')
