# 필요한 Django 패키지 설치
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "필요한 Django 패키지를 설치합니다..." -ForegroundColor Blue

# 1. 기존 Django 프로세스 종료
Write-Host "1. 기존 Django 프로세스 종료..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "pkill -f 'python manage.py runserver'"

# 2. 가상환경에서 필요한 패키지 설치
Write-Host "2. 가상환경에서 패키지 설치..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /var/www/planit && source venv/bin/activate && pip install django-crispy-forms pillow django-extensions --break-system-packages"

# 3. Django 설정 확인
Write-Host "3. Django 설정 확인..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /var/www/planit && source venv/bin/activate && python manage.py check"

# 4. 마이그레이션 실행
Write-Host "4. 마이그레이션 실행..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /var/www/planit && source venv/bin/activate && python manage.py migrate"

# 5. Django 개발 서버 재시작
Write-Host "5. Django 개발 서버 재시작..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /var/www/planit && source venv/bin/activate && nohup python manage.py runserver 0.0.0.0:8000 > server.log 2>&1 &"

Write-Host "`n✅ 패키지 설치 및 서버 재시작이 완료되었습니다!" -ForegroundColor Green
Write-Host "🌐 사이트 확인: http://planit.boramae.club/" -ForegroundColor Cyan
