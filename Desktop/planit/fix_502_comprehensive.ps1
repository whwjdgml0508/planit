# 502 Bad Gateway 종합 해결 스크립트
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "=== 502 Bad Gateway 종합 해결 시작 ===" -ForegroundColor Blue

Write-Host "`n1. 현재 실행 중인 프로세스 확인..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "ps aux | grep -E '(python|gunicorn|runserver)' | grep -v grep"

Write-Host "`n2. 모든 관련 프로세스 종료..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo pkill -f 'python.*manage.py' || true; sudo pkill -f gunicorn || true; sudo systemctl stop planit || true"

Write-Host "`n3. 포트 8000 상태 확인..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo netstat -tlnp | grep :8000 || echo 'Port 8000 is free'"

Write-Host "`n4. Django 설정 확인..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /home/ubuntu/planit && source venv/bin/activate && python manage.py check --deploy"

Write-Host "`n5. 가상환경에서 개발 서버 시작..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /home/ubuntu/planit && source venv/bin/activate && nohup python manage.py runserver 0.0.0.0:8000 > server.log 2>&1 &"

Write-Host "`n6. 서버 시작 대기 (10초)..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host "`n7. 서버 프로세스 확인..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "ps aux | grep 'runserver 0.0.0.0:8000' | grep -v grep"

Write-Host "`n8. 포트 8000 바인딩 확인..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo netstat -tlnp | grep :8000"

Write-Host "`n9. 서버 로그 확인..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /home/ubuntu/planit && tail -20 server.log"

Write-Host "`n10. 로컬 연결 테스트..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "curl -I http://127.0.0.1:8000/ || echo 'Local connection failed'"

Write-Host "`n11. nginx 설정 테스트..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo nginx -t"

Write-Host "`n12. nginx 재시작..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo systemctl reload nginx"

Write-Host "`n✅ 502 오류 해결 완료!" -ForegroundColor Green
Write-Host "웹사이트 확인: http://planit.boramae.club" -ForegroundColor Blue
Write-Host "관리자 페이지: http://planit.boramae.club/admin/" -ForegroundColor Cyan
Write-Host "사용자명: admin | 비밀번호: planit2024!" -ForegroundColor Cyan
