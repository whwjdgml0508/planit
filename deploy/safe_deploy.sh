#!/bin/bash
echo "🚀 PlanIt 안전 배포 시작..."

# 현재 디렉토리로 이동
cd /home/ubuntu/planit

# 가상환경 활성화
source /home/ubuntu/planit/planit/venv/bin/activate

# 데이터베이스 백업
echo "💾 데이터베이스 백업 중..."
python manage.py dumpdata --natural-foreign --natural-primary > backup_$(date +%Y%m%d_%H%M%S).json

# 현재 변경사항 임시 저장 (데이터베이스 파일 포함)
echo "📦 현재 변경사항 임시 저장 중..."
git add .
git stash push -m "배포 전 임시 저장 $(date)"

# 최신 코드 가져오기
echo "📥 최신 코드 가져오는 중..."
git pull origin main

# 마이그레이션 (기존 데이터 유지)
echo "🗄️ 데이터베이스 업데이트 중..."
python manage.py makemigrations
python manage.py migrate

# 정적 파일 수집
echo "📁 정적 파일 수집 중..."
python manage.py collectstatic --noinput

# 서버 재시작
echo "🔄 서버 재시작 중..."
pkill -f python
pkill -f gunicorn
nohup python manage.py runserver 127.0.0.1:8000 > server.log 2>&1 &

echo "✅ 안전 배포 완료! 데이터가 보존되었습니다."
echo "📊 서버 로그: tail -f /home/ubuntu/planit/server.log"

# 배포 후 데이터 확인
echo "🔍 배포 후 데이터 확인 중..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
from timetable.models import Subject
User = get_user_model()

print('=== 등록된 사용자 ===')
for user in User.objects.all():
    print(f'사용자: {user.username}')

print('\n=== 모든 과목들 ===')
for subject in Subject.objects.all():
    print(f'사용자: {subject.user.username}, 과목: {subject.name}, 색상: {subject.color}')

print(f'\n총 사용자: {User.objects.count()}명, 총 과목: {Subject.objects.count()}개')
"
