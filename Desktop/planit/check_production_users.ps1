# Production 서버의 사용자 목록 확인

Write-Host "=== Production 서버 사용자 확인 ===" -ForegroundColor Cyan

$command = @"
cd /home/ubuntu/planit
source venv/bin/activate
python manage.py shell << 'PYTHON'
from django.contrib.auth import get_user_model
User = get_user_model()

print('\n총 사용자 수:', User.objects.count())
print('\n등록된 사용자 목록:')
for user in User.objects.all().order_by('-date_joined'):
    print(f'\n사용자명: {user.username}')
    print(f'  학번: {user.student_id}')
    print(f'  이름: {user.last_name}{user.first_name}')
    print(f'  이메일: {user.email}')
    print(f'  가입일: {user.date_joined}')
PYTHON
"@

ssh -i ~/.ssh/ec2-kafa-2-key.pem ubuntu@35.163.12.109 $command
