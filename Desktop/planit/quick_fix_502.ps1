# 502 오류 빠른 해결
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "502 Bad Gateway 오류를 해결합니다..." -ForegroundColor Red

# 1. 서버 상태 확인
Write-Host "1. 서버 상태 확인 중..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "ps aux | grep python | grep -v grep"

# 2. 모든 프로세스 종료 후 재시작
Write-Host "2. 서버 재시작 중..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /home/ubuntu/planit && pkill -f python && pkill -f gunicorn && sleep 3 && source venv/bin/activate && nohup python manage.py runserver 0.0.0.0:8000 > server.log 2>&1 &"

# 3. nginx 재시작
Write-Host "3. nginx 재시작 중..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo systemctl restart nginx"

Write-Host "4. 서버 시작 대기 중..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# 5. 상태 확인
Write-Host "5. 최종 상태 확인..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "ps aux | grep python | grep runserver && echo '✅ Django 서버 실행 중'"

Write-Host "`n✅ 502 오류 해결 작업 완료!" -ForegroundColor Green
Write-Host "이제 웹사이트에 접속해보세요: http://planit.boramae.club" -ForegroundColor Blue
