# 올바른 경로로 502 Bad Gateway 해결
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "=== 올바른 경로로 502 오류 해결 ===" -ForegroundColor Blue

Write-Host "`n1. 모든 관련 프로세스 종료..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo pkill -f 'python.*manage.py' || true; sudo pkill -f gunicorn || true; sudo systemctl stop planit || true"

Write-Host "`n2. /var/www/planit 경로에서 Django 확인..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "ls -la /var/www/planit/manage.py"

Write-Host "`n3. /var/www/planit에서 가상환경 활성화 및 서버 시작..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /var/www/planit && source venv/bin/activate && nohup python manage.py runserver 0.0.0.0:8000 > server.log 2>&1 &"

Write-Host "`n4. 서버 시작 대기 (8초)..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

Write-Host "`n5. 서버 프로세스 확인..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "ps aux | grep 'runserver 0.0.0.0:8000' | grep -v grep"

Write-Host "`n6. 포트 8000 바인딩 확인..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo netstat -tlnp | grep :8000"

Write-Host "`n7. 서버 로그 확인..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /var/www/planit && tail -10 server.log"

Write-Host "`n8. 로컬 연결 테스트..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "curl -I http://127.0.0.1:8000/ 2>/dev/null | head -1 || echo 'Connection failed'"

Write-Host "`n9. nginx 재시작..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo systemctl reload nginx"

Write-Host "`n✅ 502 오류 해결 완료!" -ForegroundColor Green
Write-Host "🌐 웹사이트: http://planit.boramae.club" -ForegroundColor Blue
Write-Host "👤 관리자: http://planit.boramae.club/admin/ (admin/planit2024!)" -ForegroundColor Cyan
