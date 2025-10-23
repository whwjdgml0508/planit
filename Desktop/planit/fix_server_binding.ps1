# 서버 바인딩 수정으로 502 오류 해결
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "서버 바인딩을 수정하여 502 오류를 해결합니다..." -ForegroundColor Blue

Write-Host "1. 기존 프로세스 종료 중..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "pkill -f python || true"

Write-Host "2. 가상환경에서 서버를 0.0.0.0:8000으로 시작..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /home/ubuntu/planit && source venv/bin/activate && nohup python manage.py runserver 0.0.0.0:8000 > server.log 2>&1 &"

Write-Host "3. 서버 시작 대기..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

Write-Host "4. 서버 상태 확인..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "ps aux | grep 'runserver 0.0.0.0:8000'"

Write-Host "5. 포트 8000 확인..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "netstat -tlnp | grep :8000"

Write-Host "`n✅ 서버 재시작 완료!" -ForegroundColor Green
Write-Host "이제 웹사이트에 접속해보세요: http://planit.boramae.club" -ForegroundColor Blue

Write-Host "`n📋 관리자 로그인 정보:" -ForegroundColor Cyan
Write-Host "🌐 URL: http://planit.boramae.club/admin/" -ForegroundColor Cyan
Write-Host "👤 사용자명: admin" -ForegroundColor Cyan
Write-Host "🔑 비밀번호: planit2024!" -ForegroundColor Cyan
