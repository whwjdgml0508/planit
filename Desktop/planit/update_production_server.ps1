# Production 서버 업데이트 스크립트

Write-Host "=== Production 서버 업데이트 시작 ===" -ForegroundColor Green

# SSH 명령어들을 순차적으로 실행
$commands = @(
    "cd /home/ubuntu/planit",
    "git pull origin main",
    "python manage.py migrate",
    "sudo systemctl restart planit",
    "sudo systemctl restart nginx",
    "sudo systemctl status planit"
)

Write-Host "`nSSH로 서버에 접속하여 다음 명령어들을 실행하세요:" -ForegroundColor Yellow
Write-Host "ssh ubuntu@planit.boramae.club" -ForegroundColor Cyan

foreach ($cmd in $commands) {
    Write-Host $cmd -ForegroundColor White
}

Write-Host "`n또는 한 번에 실행:" -ForegroundColor Yellow
$oneLineCommand = ($commands -join " && ")
Write-Host "ssh ubuntu@planit.boramae.club '$oneLineCommand'" -ForegroundColor Cyan

Write-Host "`n업데이트 완료 후 테스트:" -ForegroundColor Green
Write-Host "https://planit.boramae.club/accounts/register/" -ForegroundColor White
