import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.production')
django.setup()

from timetable.models import TimeSlot, Semester
from accounts.models import User

print("=== TimeSlot 데이터 확인 ===")
print(f"총 TimeSlot 수: {TimeSlot.objects.count()}")

for ts in TimeSlot.objects.all():
    print(f"- {ts.subject.name} | {ts.day} | {ts.period}교시 | 학기: {ts.semester} | 사용자: {ts.subject.user.username}")

print("\n=== 학기 데이터 확인 ===")
for sem in Semester.objects.all():
    print(f"- {sem} | 현재학기: {sem.is_current} | 사용자: {sem.user.username}")
