# PlanIt 프로필 통계 기능 배포 스크립트

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "PlanIt 프로필 통계 기능 배포 시작" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# SSH 접속 정보
$SSH_KEY = "~/.ssh/ec2-kafa-2-key.pem"
$SSH_USER = "ubuntu"
$SSH_HOST = "35.163.12.109"
$PROJECT_PATH = "/home/ubuntu/planit"

Write-Host "`n1. SSH 접속 및 코드 업데이트..." -ForegroundColor Yellow

# SSH 명령어 실행
$commands = @"
cd $PROJECT_PATH && \
git pull origin main && \
echo '코드 업데이트 완료' && \
sudo systemctl restart planit && \
echo 'PlanIt 서비스 재시작 완료' && \
sudo systemctl restart nginx && \
echo 'Nginx 재시작 완료' && \
sleep 3 && \
sudo systemctl status planit --no-pager -l
"@

ssh -i $SSH_KEY "${SSH_USER}@${SSH_HOST}" $commands

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "배포 완료!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`n프로필 페이지를 확인하세요:" -ForegroundColor Yellow
Write-Host "http://planit.boramae.club/accounts/profile/" -ForegroundColor Cyan
