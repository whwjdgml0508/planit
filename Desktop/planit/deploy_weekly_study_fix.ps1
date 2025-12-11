# PlanIt 이번주 학습시간 수정 배포 스크립트

$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "c:\Users\User\.ssh\ec2-kafa-2-key.pem"

Write-Host "🚀 PlanIt 이번주 학습시간 수정 배포 시작..." -ForegroundColor Green

# 1. Git pull
Write-Host "📥 Git pull 실행 중..." -ForegroundColor Blue
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /home/ubuntu/planit && git pull origin main"

# 2. 서비스 중지
Write-Host "⏸️ 서비스 중지 중..." -ForegroundColor Blue
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo systemctl stop planit"

# 3. 파일 권한 설정
Write-Host "🔐 파일 권한 설정 중..." -ForegroundColor Blue
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo chown -R ubuntu:ubuntu /home/ubuntu/planit"

# 4. 서버 재시작
Write-Host "🔄 서버 재시작 중..." -ForegroundColor Blue
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo systemctl restart planit && sudo systemctl restart nginx"

# 5. 서비스 상태 확인
Write-Host "✅ 서비스 상태 확인 중..." -ForegroundColor Blue
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo systemctl status planit --no-pager -l | head -20"

Write-Host "✅ 배포 완료!" -ForegroundColor Green
Write-Host "🌐 웹사이트 확인: http://planit.boramae.club/planner/" -ForegroundColor Cyan
