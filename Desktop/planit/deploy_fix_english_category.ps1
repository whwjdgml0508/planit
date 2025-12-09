# 영어상식 카테고리 추가 및 배포 스크립트

Write-Host "=" -ForegroundColor Cyan
Write-Host "영어상식 카테고리 추가 및 배포" -ForegroundColor Cyan
Write-Host "=" -ForegroundColor Cyan

# 1. Git 커밋 및 푸시
Write-Host "`n1. Git 커밋 및 푸시..." -ForegroundColor Yellow
git add .
git commit -m "Add: 영어상식 카테고리 추가 및 카테고리 카드 UI 개선"
git push origin main

# 2. SSH로 서버 접속하여 업데이트
Write-Host "`n2. 서버 업데이트 중..." -ForegroundColor Yellow

$sshCommand = @"
cd /home/ubuntu/planit && \
git pull origin main && \
source venv/bin/activate && \
python add_english_category.py && \
sudo systemctl restart planit && \
sudo systemctl restart nginx && \
echo '✅ 배포 완료!'
"@

ssh -i ~/.ssh/ec2-kafa-2-key.pem ubuntu@35.163.12.109 $sshCommand

Write-Host "`n✅ 모든 작업 완료!" -ForegroundColor Green
Write-Host "웹사이트를 확인하세요: http://planit.boramae.club/community/" -ForegroundColor Cyan
