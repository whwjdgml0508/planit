import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.production')
django.setup()

from timetable.models import TimeSlot, Semester, Subject
from accounts.models import User

username = "75.1.조정희"
user = User.objects.get(username=username)

print(f"=== 사용자: {username} ===")
print(f"User ID: {user.id}")

# 사용자의 현재 학기
current_semester = Semester.objects.filter(user=user, is_current=True).first()
print(f"\n현재 학기: {current_semester}")
if current_semester:
    print(f"학기 ID: {current_semester.id}")

# 사용자의 과목들
subjects = Subject.objects.filter(user=user)
print(f"\n과목 수: {subjects.count()}")
for s in subjects:
    print(f"  - {s.name} (ID: {s.id})")

# 사용자의 TimeSlot (semester 필터 없이)
all_slots = TimeSlot.objects.filter(subject__user=user)
print(f"\n전체 TimeSlot 수: {all_slots.count()}")
for ts in all_slots:
    print(f"  - {ts.subject.name} | {ts.day} {ts.period}교시 | semester_id: {ts.semester_id}")

# 현재 학기로 필터링한 TimeSlot
if current_semester:
    filtered_slots = TimeSlot.objects.filter(subject__user=user, semester=current_semester)
    print(f"\n현재 학기 TimeSlot 수: {filtered_slots.count()}")
    for ts in filtered_slots:
        print(f"  - {ts.subject.name} | {ts.day} {ts.period}교시")
