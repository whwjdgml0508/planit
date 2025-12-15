import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.development')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

print("=" * 60)
print("팀원 계정 일괄 생성")
print("=" * 60)

# 팀원 정보 입력 (예시)
team_members = [
    {
        'username': '조정희',
        'student_id': '7513825',
        'first_name': '정희',
        'last_name': '조',
        'email': 'student7513825@example.com',
        'department': 'CS',  # 컴퓨터공학과
        'grade': '1',
        'password': 'planit2024!',  # 임시 비밀번호 (나중에 변경하세요)
    },
    # 다른 팀원 추가
    # {
    #     'username': '팀원2',
    #     'student_id': '7513826',
    #     'first_name': '이름',
    #     'last_name': '성',
    #     'email': 'student7513826@example.com',
    #     'department': 'CS',
    #     'grade': '1',
    #     'password': 'planit2024!',
    # },
]

print("\n다음 계정들을 생성합니다:")
for idx, member in enumerate(team_members, 1):
    print(f"\n{idx}. {member['last_name']}{member['first_name']} (학번: {member['student_id']})")

confirm = input("\n계속하시겠습니까? (y/n): ").strip().lower()

if confirm == 'y':
    created_count = 0
    for member in team_members:
        try:
            # 이미 존재하는지 확인
            if User.objects.filter(student_id=member['student_id']).exists():
                print(f"\n✗ {member['student_id']} - 이미 존재하는 학번입니다.")
                continue
            
            if User.objects.filter(username=member['username']).exists():
                print(f"\n✗ {member['username']} - 이미 존재하는 사용자명입니다.")
                continue
            
            # 사용자 생성
            user = User.objects.create_user(
                username=member['username'],
                student_id=member['student_id'],
                first_name=member['first_name'],
                last_name=member['last_name'],
                email=member['email'],
                department=member['department'],
                grade=member['grade'],
                password=member['password']
            )
            
            print(f"\n✓ {member['last_name']}{member['first_name']} 계정 생성 완료!")
            print(f"  - 사용자명: {user.username}")
            print(f"  - 학번: {user.student_id}")
            print(f"  - 임시 비밀번호: {member['password']}")
            created_count += 1
            
        except Exception as e:
            print(f"\n✗ {member['last_name']}{member['first_name']} 생성 실패: {str(e)}")
    
    print(f"\n{'=' * 60}")
    print(f"총 {created_count}개 계정 생성 완료!")
    print(f"{'=' * 60}")
    print("\n⚠️  중요: 첫 로그인 후 반드시 비밀번호를 변경하세요!")
else:
    print("\n취소되었습니다.")

print("\n" + "=" * 60)
