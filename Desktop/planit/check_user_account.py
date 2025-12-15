import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.development')
django.setup()

from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

print("=" * 60)
print("사용자 계정 확인")
print("=" * 60)

# 75.1.조정희 계정 검색
search_terms = ['75.1.조정희', '조정희', '751조정희', '751']

print("\n검색 중...")
for term in search_terms:
    users = User.objects.filter(
        Q(username__icontains=term) | 
        Q(first_name__icontains=term) | 
        Q(last_name__icontains=term) |
        Q(student_id__icontains=term)
    )
    if users.exists():
        print(f"\n'{term}' 검색 결과:")
        for user in users:
            print(f"\n  사용자 정보:")
            print(f"  - 사용자명: {user.username}")
            print(f"  - 이름: {user.last_name}{user.first_name}")
            print(f"  - 학번: {user.student_id}")
            print(f"  - 이메일: {user.email}")
            print(f"  - 학과: {user.get_department_display()}")
            print(f"  - 학년: {user.get_grade_display()}")
            print(f"  - 활성 상태: {user.is_active}")
            print(f"  - 가입일: {user.date_joined}")

# 모든 사용자 목록
print("\n" + "=" * 60)
print("전체 등록 사용자 목록:")
print("=" * 60)
all_users = User.objects.all().order_by('-date_joined')
if all_users.exists():
    for idx, user in enumerate(all_users, 1):
        print(f"{idx}. {user.username} ({user.last_name}{user.first_name}) - 학번: {user.student_id}")
else:
    print("등록된 사용자가 없습니다.")

print("\n" + "=" * 60)
