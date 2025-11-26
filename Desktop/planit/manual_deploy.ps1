# 수동 배포 스크립트 - 각 명령을 개별적으로 실행
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "수동으로 배포를 진행합니다..." -ForegroundColor Blue

# 1. 프로젝트 디렉토리로 이동 및 코드 업데이트
Write-Host "1. 코드 업데이트 중..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /home/ubuntu/planit && git pull origin main"

# 2. 가상환경에서 의존성 설치
Write-Host "2. 의존성 설치 중..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /home/ubuntu/planit && source venv/bin/activate && pip install -r requirements.txt --break-system-packages"

# 3. Django 마이그레이션
Write-Host "3. Django 마이그레이션 중..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /home/ubuntu/planit && source venv/bin/activate && python manage.py migrate"

# 4. 정적 파일 수집
Write-Host "4. 정적 파일 수집 중..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /home/ubuntu/planit && source venv/bin/activate && python manage.py collectstatic --noinput"

# 5. Gunicorn 서비스 재시작
Write-Host "5. 서비스 재시작 중..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo systemctl daemon-reload && sudo systemctl restart planit && sudo systemctl restart nginx"

# 6. 서비스 상태 확인
Write-Host "6. 서비스 상태 확인 중..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo systemctl status planit"

Write-Host "`n✅ 배포가 완료되었습니다!" -ForegroundColor Green
Write-Host "🌐 사이트 확인: http://planit.boramae.club/" -ForegroundColor Cyan
