# 수정된 코드를 서버에 배포
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "수정된 코드를 서버에 배포합니다..." -ForegroundColor Blue

# 1. 기존 Django 프로세스 종료
Write-Host "1. 기존 Django 프로세스 종료..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "pkill -f 'python manage.py runserver'"

# 2. Git을 통해 최신 코드 가져오기
Write-Host "2. 최신 코드 가져오기..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /var/www/planit && git pull origin main"

# 3. Django 개발 서버 재시작
Write-Host "3. Django 개발 서버 재시작..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /var/www/planit && source venv/bin/activate && nohup python manage.py runserver 0.0.0.0:8000 > server.log 2>&1 &"

Write-Host "`n✅ 코드 배포가 완료되었습니다!" -ForegroundColor Green
Write-Host "🌐 사이트에서 과목 색상 변경을 시도해보세요: http://planit.boramae.club/" -ForegroundColor Cyan
Write-Host "📋 이제 구체적인 오류 메시지가 표시됩니다." -ForegroundColor Yellow
