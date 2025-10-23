# 502 오류 해결을 위한 종합 스크립트
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "=== 502 Bad Gateway 오류 해결 시작 ===" -ForegroundColor Blue

Write-Host "`n1. 현재 실행 중인 프로세스 확인..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "ps aux | grep python"

Write-Host "`n2. 포트 8000 사용 상태 확인..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "netstat -tlnp | grep :8000 || echo 'Port 8000 not in use'"

Write-Host "`n3. 모든 Python 프로세스 종료..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo pkill -f python || true"

Write-Host "`n4. 가상환경 활성화 및 Django 서버 시작..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /home/ubuntu/planit && source venv/bin/activate && nohup python manage.py runserver 0.0.0.0:8000 > server.log 2>&1 &"

Write-Host "`n5. 서버 시작 대기 (10초)..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host "`n6. 서버 프로세스 확인..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "ps aux | grep 'runserver 0.0.0.0:8000' | grep -v grep"

Write-Host "`n7. 포트 8000 바인딩 확인..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "netstat -tlnp | grep :8000"

Write-Host "`n8. 서버 로그 확인..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /home/ubuntu/planit && tail -20 server.log"

Write-Host "`n9. nginx 상태 확인..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo systemctl status nginx"

Write-Host "`n10. nginx 재시작..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo systemctl restart nginx"

Write-Host "`n=== 해결 완료! ===" -ForegroundColor Green
Write-Host "웹사이트 접속: http://planit.boramae.club" -ForegroundColor Blue
Write-Host "관리자 페이지: http://planit.boramae.club/admin/" -ForegroundColor Blue
Write-Host "사용자명: admin" -ForegroundColor Cyan
Write-Host "비밀번호: planit2024!" -ForegroundColor Cyan
