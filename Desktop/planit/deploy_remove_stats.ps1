# PlanIt - 나의 학습 현황 섹션 제거 배포 스크립트

Write-Host "=== PlanIt 나의 학습 현황 제거 배포 시작 ===" -ForegroundColor Green

# 1. Git 변경사항 추가
Write-Host "`n1. Git 변경사항 추가 중..." -ForegroundColor Yellow
git add templates/home.html

# 2. 커밋
Write-Host "`n2. 변경사항 커밋 중..." -ForegroundColor Yellow
git commit -m "Remove 나의 학습 현황 section from home page"

# 3. GitHub에 푸시
Write-Host "`n3. GitHub에 푸시 중..." -ForegroundColor Yellow
git push origin main

# 4. SSH로 서버 접속하여 배포
Write-Host "`n4. Production 서버에 배포 중..." -ForegroundColor Yellow
ssh -i ~/.ssh/ec2-kafa-2-key.pem ubuntu@35.163.12.109 @"
    cd /home/ubuntu/planit && \
    echo '=== Git Pull ===' && \
    git pull origin main && \
    echo '=== 서비스 재시작 ===' && \
    sudo systemctl restart planit && \
    sudo systemctl restart nginx && \
    echo '=== 배포 완료 ===' && \
    sudo systemctl status planit --no-pager -l
"@

Write-Host "`n=== 배포 완료! ===" -ForegroundColor Green
Write-Host "웹사이트 확인: http://planit.boramae.club/" -ForegroundColor Cyan
