# 과목 수정 오류 확인 스크립트
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "과목 수정 오류를 확인합니다..." -ForegroundColor Blue

# 1. Django 서버 로그 확인
Write-Host "1. Django 서버 로그 확인..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /var/www/planit && tail -50 server.log"

# 2. Django 폼 검증 테스트
Write-Host "2. Django 폼 검증 테스트..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /var/www/planit && source venv/bin/activate && python manage.py shell -c \"
from timetable.forms import SubjectForm
from timetable.models import Subject
from django.contrib.auth.models import User

# 테스트 데이터로 폼 검증
test_data = {
    'name': '테스트 과목',
    'professor': '테스트 교수',
    'credits': 3,
    'subject_type': 'MAJOR',
    'color': '#ff0000'
}

form = SubjectForm(data=test_data)
print('폼 유효성:', form.is_valid())
if not form.is_valid():
    print('폼 오류:', form.errors)
\""
