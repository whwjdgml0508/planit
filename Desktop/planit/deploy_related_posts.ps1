# Production 서버에 관련 게시글 기능 배포

$serverUser = "ubuntu"
$serverIP = "35.163.12.109"
$keyPath = "$env:USERPROFILE\.ssh\ec2-kafa-2-key.pem"

Write-Host "=== PlanIt 관련 게시글 기능 배포 ===" -ForegroundColor Green

# 1. views.py 파일 복사
Write-Host "`n1. views.py 파일 복사 중..." -ForegroundColor Yellow
scp -i $keyPath community/views.py "${serverUser}@${serverIP}:/home/ubuntu/planit/community/"

# 2. post_detail.html 파일 복사
Write-Host "`n2. post_detail.html 파일 복사 중..." -ForegroundColor Yellow
scp -i $keyPath templates/community/post_detail.html "${serverUser}@${serverIP}:/home/ubuntu/planit/templates/community/"

# 3. 서버 재시작
Write-Host "`n3. 서버 재시작 중..." -ForegroundColor Yellow
ssh -i $keyPath "${serverUser}@${serverIP}" "sudo systemctl restart planit && sudo systemctl restart nginx"

Write-Host "`n=== 배포 완료! ===" -ForegroundColor Green
Write-Host "http://planit.boramae.club 에서 확인하세요." -ForegroundColor Cyan
