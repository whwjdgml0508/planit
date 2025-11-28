# PlanIt 서버 배포 스크립트 (PowerShell)

$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "c:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "🚀 PlanIt 서버 배포 시작..." -ForegroundColor Green

# SSH 키 권한 확인
Write-Host "📋 SSH 키 권한 확인 중..." -ForegroundColor Blue
if (Test-Path $SSH_KEY_PATH) {
    Write-Host "✅ SSH 키 파일 발견: $SSH_KEY_PATH" -ForegroundColor Green
} else {
    Write-Host "❌ SSH 키 파일을 찾을 수 없습니다: $SSH_KEY_PATH" -ForegroundColor Red
    exit 1
}

# 서버에 SSH 접속하여 배포 명령 실행
Write-Host "📡 서버에 접속하여 배포 중..." -ForegroundColor Blue

$deployCommands = @"
cd /var/www/planit
echo '📥 최신 코드 가져오는 중...'
git pull origin main
echo '🔧 가상환경 활성화 중...'
source venv/bin/activate
echo '🗄️ 데이터베이스 마이그레이션 실행 중...'
python manage.py migrate
echo '📁 정적 파일 수집 중...'
python manage.py collectstatic --noinput
echo '🔄 서버 재시작 중...'
sudo systemctl restart planit
sudo systemctl restart nginx
echo '✅ 배포 완료!'
"@

# SSH 명령 실행
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP $deployCommands

if ($LASTEXITCODE -eq 0) {
    Write-Host "🎉 배포가 성공적으로 완료되었습니다!" -ForegroundColor Green
    Write-Host "🌐 웹사이트 확인: http://planit.boramae.club" -ForegroundColor Cyan
    Write-Host "📋 학기 관리 페이지: http://planit.boramae.club/timetable/semester/create/" -ForegroundColor Cyan
} else {
    Write-Host "❌ 배포 중 오류가 발생했습니다." -ForegroundColor Red
}
