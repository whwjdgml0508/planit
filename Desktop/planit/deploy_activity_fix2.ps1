# PlanIt 최근 활동 기능 수정 배포 스크립트 v2

$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "c:\Users\User\.ssh\ec2-kafa-2-key.pem"

Write-Host "🚀 PlanIt 최근 활동 기능 수정 배포 시작..." -ForegroundColor Green

# 1. Git pull
Write-Host "📥 Git pull 실행 중..." -ForegroundColor Blue
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /var/www/planit && git pull origin main"

# 2. accounts/views.py 파일 복사 (올바른 경로)
Write-Host "📁 accounts/views.py 파일 복사 중..." -ForegroundColor Blue
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo cp /var/www/planit/Desktop/planit/accounts/views.py /home/ubuntu/planit/accounts/views.py"

# 3. 템플릿 파일 복사 (올바른 경로)
Write-Host "📁 템플릿 파일 복사 중..." -ForegroundColor Blue
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo cp /var/www/planit/Desktop/planit/templates/accounts/profile.html /home/ubuntu/planit/templates/accounts/profile.html"

# 4. 파일 권한 설정
Write-Host "🔐 파일 권한 설정 중..." -ForegroundColor Blue
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo chown ubuntu:ubuntu /home/ubuntu/planit/accounts/views.py /home/ubuntu/planit/templates/accounts/profile.html"

# 5. 서버 재시작
Write-Host "🔄 서버 재시작 중..." -ForegroundColor Blue
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo systemctl restart planit && sudo systemctl restart nginx"

# 6. 서비스 상태 확인
Write-Host "✅ 서비스 상태 확인 중..." -ForegroundColor Blue
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo systemctl status planit --no-pager -l | head -20"

Write-Host "✅ 배포 완료!" -ForegroundColor Green
Write-Host "🌐 웹사이트 확인: http://planit.boramae.club/accounts/profile/" -ForegroundColor Cyan
