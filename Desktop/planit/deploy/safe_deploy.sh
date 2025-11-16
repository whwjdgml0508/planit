#!/bin/bash
echo "🚀 PlanIt 안전 배포 시작..."

# 현재 디렉토리로 이동
cd /home/ubuntu/planit

# 가상환경 활성화
source /home/ubuntu/planit/planit/venv/bin/activate

# 김공군 계정 데이터 특별 백업
echo "👤 김공군 계정 데이터 백업 중..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
from timetable.models import Subject
import json
User = get_user_model()

try:
    kim_user = User.objects.get(username='김공군')
    subjects = Subject.objects.filter(user=kim_user)
    
    backup_data = {
        'user': {
            'username': kim_user.username,
            'first_name': kim_user.first_name,
            'last_name': kim_user.last_name,
            'email': kim_user.email
        },
        'subjects': []
    }
    
    for subject in subjects:
        backup_data['subjects'].append({
            'name': subject.name,
            'color': subject.color,
            'subject_type': subject.subject_type
        })
    
    with open('kim_backup.json', 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, ensure_ascii=False, indent=2)
    
    print(f'김공군 계정 백업 완료: {len(backup_data[\"subjects\"])}개 과목')
except Exception as e:
    print(f'김공군 계정 백업 실패: {e}')
"

# 전체 데이터베이스 백업
echo "💾 전체 데이터베이스 백업 중..."
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

# 김공군 계정 복구
echo "👤 김공군 계정 복구 중..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
from timetable.models import Subject
import json
import os
User = get_user_model()

if os.path.exists('kim_backup.json'):
    try:
        with open('kim_backup.json', 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
        
        # 김공군 계정 생성/업데이트
        user, created = User.objects.get_or_create(
            username=backup_data['user']['username'],
            defaults=backup_data['user']
        )
        
        if created:
            print('김공군 계정을 새로 생성했습니다.')
        else:
            print('김공군 계정이 이미 존재합니다.')
        
        # 과목 복구
        restored_count = 0
        for subject_data in backup_data['subjects']:
            subject, created = Subject.objects.get_or_create(
                user=user,
                name=subject_data['name'],
                defaults=subject_data
            )
            if created:
                restored_count += 1
        
        print(f'과목 복구 완료: {restored_count}개 새로 생성')
        print(f'김공군 계정의 총 과목 수: {Subject.objects.filter(user=user).count()}개')
        
    except Exception as e:
        print(f'김공군 계정 복구 실패: {e}')
else:
    print('김공군 백업 파일이 없습니다.')
"

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

print('\n=== 김공군 계정의 과목들 ===')
try:
    kim_user = User.objects.get(username='김공군')
    subjects = Subject.objects.filter(user=kim_user)
    for subject in subjects:
        print(f'- {subject.name}: {subject.color} ({subject.subject_type})')
    print(f'총 {subjects.count()}개 과목')
except:
    print('김공군 계정을 찾을 수 없습니다.')

print(f'\n전체 통계: 사용자 {User.objects.count()}명, 과목 {Subject.objects.count()}개')
"