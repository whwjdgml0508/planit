import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.development')
django.setup()

from django.contrib.auth import get_user_model, authenticate
from django.db.models import Q

User = get_user_model()

print("=" * 60)
print("로그인 디버깅 테스트")
print("=" * 60)

# 모든 사용자 목록 출력
print("\n[1] 등록된 사용자 목록:")
users = User.objects.all()
if users.exists():
    for user in users:
        print(f"  - 사용자명: {user.username}, 학번: {user.student_id}, 활성: {user.is_active}")
else:
    print("  등록된 사용자가 없습니다.")

# 사용자 입력 받기
print("\n[2] 로그인 테스트")
username_input = input("사용자명 또는 학번을 입력하세요: ").strip()
password_input = input("비밀번호를 입력하세요: ").strip()

# 사용자 찾기
print(f"\n[3] '{username_input}' 사용자 검색 중...")
try:
    user = User.objects.get(Q(username=username_input) | Q(student_id=username_input))
    print(f"✓ 사용자 발견: {user.username} (ID: {user.id})")
    print(f"  - 학번: {user.student_id}")
    print(f"  - 이메일: {user.email}")
    print(f"  - 활성 상태: {user.is_active}")
    print(f"  - 슈퍼유저: {user.is_superuser}")
    print(f"  - 스태프: {user.is_staff}")
    
    # 비밀번호 확인
    print(f"\n[4] 비밀번호 검증 중...")
    if user.check_password(password_input):
        print("✓ 비밀번호 일치!")
    else:
        print("✗ 비밀번호 불일치!")
        print("\n비밀번호 해시 정보:")
        print(f"  - 저장된 해시: {user.password[:50]}...")
        
    # Django 인증 시스템 테스트
    print(f"\n[5] Django 인증 시스템 테스트...")
    authenticated_user = authenticate(username=username_input, password=password_input)
    if authenticated_user:
        print(f"✓ 인증 성공: {authenticated_user.username}")
    else:
        print("✗ 인증 실패!")
        
except User.DoesNotExist:
    print(f"✗ '{username_input}' 사용자를 찾을 수 없습니다.")
    print("\n유사한 사용자명 검색:")
    similar_users = User.objects.filter(
        Q(username__icontains=username_input) | Q(student_id__icontains=username_input)
    )
    if similar_users.exists():
        for u in similar_users:
            print(f"  - {u.username} (학번: {u.student_id})")
    else:
        print("  유사한 사용자가 없습니다.")
except User.MultipleObjectsReturned:
    print(f"✗ 여러 사용자가 발견되었습니다. (데이터 무결성 문제)")
    users = User.objects.filter(Q(username=username_input) | Q(student_id=username_input))
    for u in users:
        print(f"  - {u.username} (학번: {u.student_id})")

print("\n" + "=" * 60)
