#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.production')
django.setup()

from timetable.models import Subject, Semester, TimeSlot

# 현재 학기 찾기
current = Semester.objects.filter(is_current=True).first()
print(f"현재 학기: {current}")

# 학기 미지정 TimeSlot들을 현재 학기에 할당
unassigned_slots = TimeSlot.objects.filter(semester__isnull=True)
print(f"학기 미지정 TimeSlot 수: {unassigned_slots.count()}")

if current and unassigned_slots.exists():
    updated = unassigned_slots.update(semester=current)
    print(f"{updated}개 TimeSlot을 현재 학기에 할당했습니다.")
else:
    print("할당할 TimeSlot이 없거나 현재 학기가 설정되지 않았습니다.")

# 결과 확인
print(f"\n=== 결과 ===")
print(f"전체 과목: {Subject.objects.count()}개")
print(f"전체 TimeSlot: {TimeSlot.objects.count()}개")
print(f"현재 학기 TimeSlot: {TimeSlot.objects.filter(semester=current).count()}개")
