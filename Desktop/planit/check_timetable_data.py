#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.production')
django.setup()

from accounts.models import User
from timetable.models import Subject, TimeSlot

# 모든 사용자 출력 및 과목 개수 확인
print("All users in database:")
all_users = User.objects.all()
user_with_subjects = None
for u in all_users:
    subject_count = Subject.objects.filter(user=u).count()
    print(f"  - {u.username} (학번: {u.student_id}) - {subject_count}개 과목")
    if subject_count > 0 and user_with_subjects is None:
        user_with_subjects = u
print("-" * 50)

# 과목이 있는 사용자 선택
if user_with_subjects:
    user = user_with_subjects
    print(f"Selected User: {user.username} ({user.student_id})")
    print("-" * 50)
else:
    print("No users with subjects found!")
    exit()

# 모든 과목 조회
subjects = Subject.objects.filter(user=user).prefetch_related('time_slots')
print(f"Total subjects: {subjects.count()}")
print("-" * 50)

# 각 과목의 시간표 슬롯 출력
for subject in subjects:
    print(f"\n과목: {subject.name}")
    print(f"  색상: {subject.color}")
    print(f"  학기: {subject.semester}")
    time_slots = subject.time_slots.all()
    print(f"  시간표 슬롯 개수: {time_slots.count()}")
    for ts in time_slots:
        print(f"    - {ts.get_day_display()} {ts.period}교시 ({ts.location})")

print("\n" + "=" * 50)
print("시간표 데이터 구조:")
print("=" * 50)

# 시간표 데이터 구성 (views.py와 동일한 로직)
timetable_data = {}
days = ['MON', 'TUE', 'WED', 'THU', 'FRI']
periods = range(1, 9)

for day in days:
    timetable_data[day] = {}
    for period in periods:
        timetable_data[day][period] = None

for subject in subjects:
    for time_slot in subject.time_slots.all():
        if time_slot.day in timetable_data and time_slot.period in periods:
            timetable_data[time_slot.day][time_slot.period] = {
                'subject': subject,
                'time_slot': time_slot
            }

# 시간표 출력
for day in days:
    day_name = {'MON': '월', 'TUE': '화', 'WED': '수', 'THU': '목', 'FRI': '금'}[day]
    for period in periods:
        slot = timetable_data[day][period]
        if slot:
            print(f"{day_name}요일 {period}교시: {slot['subject'].name}")
