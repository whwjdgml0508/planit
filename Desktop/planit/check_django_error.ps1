# Django 오류 확인 및 수정 스크립트
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "Django 오류를 확인하고 수정합니다..." -ForegroundColor Blue

# 1. 서버 로그 확인
Write-Host "1. 서버 로그 확인..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /var/www/planit && cat server.log"

# 2. Django 설정 확인
Write-Host "2. Django 설정 확인..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /var/www/planit && python manage.py check"

# 3. 프로세스 확인
Write-Host "3. 실행 중인 Django 프로세스 확인..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "ps aux | grep python"

# 4. 포트 8000 확인
Write-Host "4. 포트 8000 상태 확인..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "netstat -tlnp | grep 8000"

# 5. Django를 직접 실행해보기
Write-Host "5. Django를 직접 실행..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /var/www/planit && timeout 10s python manage.py runserver 0.0.0.0:8000 || echo 'Django 실행 중 오류 발생'"
