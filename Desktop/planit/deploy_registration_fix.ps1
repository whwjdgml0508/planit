# Production 서버에 회원가입 수정사항 배포 스크립트

Write-Host "=== PlanIt Production 회원가입 수정사항 배포 ===" -ForegroundColor Green

# 1. 현재 변경사항 확인
Write-Host "`n1. 로컬 변경사항 확인..." -ForegroundColor Yellow
git status
git diff HEAD~1 --name-only

# 2. 변경사항 커밋 (아직 안했다면)
Write-Host "`n2. 변경사항 커밋..." -ForegroundColor Yellow
git add accounts/models.py
git add accounts/forms.py
git add accounts/views.py
git add accounts/migrations/0003_alter_user_phone_number.py
git add planit_project/settings/development.py
git commit -m "Fix registration Server Error (500) - Remove phone number validation"

# 3. Production 서버에 배포
Write-Host "`n3. Production 서버에 배포..." -ForegroundColor Yellow
git push origin main

Write-Host "`n4. SSH로 서버 접속하여 업데이트 필요:" -ForegroundColor Cyan
Write-Host "ssh ubuntu@planit.boramae.club" -ForegroundColor White
Write-Host "cd /home/ubuntu/planit" -ForegroundColor White
Write-Host "git pull origin main" -ForegroundColor White
Write-Host "python manage.py migrate" -ForegroundColor White
Write-Host "sudo systemctl restart planit" -ForegroundColor White
Write-Host "sudo systemctl restart nginx" -ForegroundColor White

Write-Host "`n배포 완료 후 https://planit.boramae.club/accounts/register/ 에서 테스트하세요." -ForegroundColor Green
