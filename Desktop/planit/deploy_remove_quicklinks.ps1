# 빠른 링크 제거 배포 스크립트

$SERVER = "ubuntu@35.163.12.109"
$KEY = "$env:USERPROFILE\.ssh\ec2-kafa-2-key.pem"
$REMOTE_PATH = "/home/ubuntu/planit"

Write-Host "🚀 커뮤니티 빠른 링크 제거 배포 시작..." -ForegroundColor Green

# SSH로 서버에 접속하여 파일 업데이트
ssh -i $KEY $SERVER @"
cd $REMOTE_PATH
git stash
git pull origin main
sudo systemctl restart planit
sudo systemctl restart nginx
echo '✅ 서버 재시작 완료'
"@

Write-Host "✅ 배포 완료!" -ForegroundColor Green
Write-Host "🌐 http://planit.boramae.club 에서 확인하세요" -ForegroundColor Cyan
