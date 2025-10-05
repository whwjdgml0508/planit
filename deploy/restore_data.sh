#!/bin/bash
echo "🔄 PlanIt 데이터 복구 시작..."

# 현재 디렉토리로 이동
cd /home/ubuntu/planit

# 가상환경 활성화
source /home/ubuntu/planit/planit/venv/bin/activate

# 김공군 계정 및 기본 과목 생성
echo "👤 김공군 계정 및 과목 생성 중..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
from timetable.models import Subject
User = get_user_model()

# 김공군 계정 생성 (이미 있으면 가져오기)
user, created = User.objects.get_or_create(
    username='김공군',
    defaults={
        'password': 'pbkdf2_sha256\$600000\$dummy\$dummy',  # 임시 비밀번호
        'first_name': '김',
        'last_name': '공군',
        'email': 'kim@example.com'
    }
)

if created:
    print('✅ 김공군 계정을 새로 생성했습니다.')
else:
    print('✅ 김공군 계정이 이미 존재합니다.')

# 기본 과목들 추가
subjects_data = [
    {'name': '수학', 'color': '#ff6b6b', 'subject_type': 'MAJOR'},
    {'name': '국어', 'color': '#4ecdc4', 'subject_type': 'GENERAL'},
    {'name': '영어', 'color': '#45b7d1', 'subject_type': 'GENERAL'},
    {'name': '역사', 'color': '#f9ca24', 'subject_type': 'GENERAL'},
    {'name': '과학', 'color': '#6c5ce7', 'subject_type': 'MAJOR'},
    {'name': '군사학', 'color': '#a0a0a0', 'subject_type': 'MILITARY'},
    {'name': '체육', 'color': '#00d2d3', 'subject_type': 'PHYSICAL'},
    {'name': '기타', 'color': '#2ed573', 'subject_type': 'OTHER'},
]

created_count = 0
for subject_data in subjects_data:
    subject, created = Subject.objects.get_or_create(
        user=user,
        name=subject_data['name'],
        defaults=subject_data
    )
    if created:
        created_count += 1
        print(f'✅ 과목 추가: {subject.name} ({subject.color})')
    else:
        print(f'ℹ️  과목 존재: {subject.name}')

print(f'\n📊 결과:')
print(f'- 새로 생성된 과목: {created_count}개')
print(f'- 김공군 계정의 총 과목 수: {Subject.objects.filter(user=user).count()}개')
print(f'- 전체 사용자 수: {User.objects.count()}명')
print(f'- 전체 과목 수: {Subject.objects.count()}개')
"

echo "✅ 데이터 복구 완료!"
