# 간단한 Admin 계정 생성
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "Admin 계정을 생성합니다..." -ForegroundColor Blue

# 1. setuptools 설치
Write-Host "1. setuptools 설치 중..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /home/ubuntu/planit && source venv/bin/activate && pip install setuptools"

# 2. Admin 계정 생성
Write-Host "2. Admin 계정 생성 중..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /home/ubuntu/planit && source venv/bin/activate && python admin_creator.py"

# 3. 서버 재시작
Write-Host "3. 서버 재시작 중..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /home/ubuntu/planit && pkill -f python || true && sleep 3 && source venv/bin/activate && nohup python manage.py runserver 0.0.0.0:8000 > server.log 2>&1 &"

Write-Host "`n✅ 작업 완료!" -ForegroundColor Green
Write-Host "`n📋 로그인 정보:" -ForegroundColor Blue
Write-Host "🌐 URL: http://planit.boramae.club/admin/" -ForegroundColor Cyan
Write-Host "👤 사용자명: admin" -ForegroundColor Cyan
Write-Host "🔑 비밀번호: planit2024!" -ForegroundColor Cyan

Write-Host "`n💡 이제 위 정보로 관리자 페이지에 로그인할 수 있습니다!" -ForegroundColor Green
