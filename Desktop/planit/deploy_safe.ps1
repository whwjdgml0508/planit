# PlanIt 안전 배포 스크립트 (PowerShell)
# templatetags 및 모든 필수 파일을 확실하게 복사

$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "~/.ssh/ec2-kafa-2-key.pem"
$REMOTE_PATH = "/home/ubuntu/planit"

Write-Host "🚀 PlanIt 안전 배포 시작..." -ForegroundColor Green

# 1. 필수 디렉토리 및 파일 복사
Write-Host "📁 필수 파일 복사 중..." -ForegroundColor Blue

# templatetags 디렉토리 복사
Write-Host "  - timetable/templatetags 복사 중..." -ForegroundColor Cyan
scp -i $SSH_KEY_PATH -r timetable/templatetags/* ${EC2_USER}@${EC2_IP}:${REMOTE_PATH}/timetable/templatetags/

Write-Host "  - planner/templatetags 복사 중..." -ForegroundColor Cyan
scp -i $SSH_KEY_PATH -r planner/templatetags/* ${EC2_USER}@${EC2_IP}:${REMOTE_PATH}/planner/templatetags/

# 주요 Python 파일 복사
Write-Host "  - 주요 Python 파일 복사 중..." -ForegroundColor Cyan
scp -i $SSH_KEY_PATH timetable/*.py ${EC2_USER}@${EC2_IP}:${REMOTE_PATH}/timetable/
scp -i $SSH_KEY_PATH planner/*.py ${EC2_USER}@${EC2_IP}:${REMOTE_PATH}/planner/
scp -i $SSH_KEY_PATH community/*.py ${EC2_USER}@${EC2_IP}:${REMOTE_PATH}/community/
scp -i $SSH_KEY_PATH accounts/*.py ${EC2_USER}@${EC2_IP}:${REMOTE_PATH}/accounts/

# 템플릿 파일 복사
Write-Host "  - 템플릿 파일 복사 중..." -ForegroundColor Cyan
scp -i $SSH_KEY_PATH -r templates/* ${EC2_USER}@${EC2_IP}:${REMOTE_PATH}/templates/

# 2. 서버에서 마이그레이션 및 재시작
Write-Host "🔧 서버 설정 및 재시작 중..." -ForegroundColor Blue

$deployCommands = @"
cd $REMOTE_PATH
echo '🗄️ 데이터베이스 마이그레이션 실행 중...'
source venv/bin/activate
python manage.py migrate
echo '📁 정적 파일 수집 중...'
python manage.py collectstatic --noinput
echo '🔄 서버 재시작 중...'
sudo systemctl restart planit
sudo systemctl restart nginx
echo '✅ 배포 완료!'
echo '📊 서비스 상태 확인...'
sudo systemctl status planit --no-pager | head -15
"@

ssh -i $SSH_KEY_PATH ${EC2_USER}@${EC2_IP} $deployCommands

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "🎉 배포가 성공적으로 완료되었습니다!" -ForegroundColor Green
    Write-Host "🌐 웹사이트: http://planit.boramae.club" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📋 주요 페이지 테스트 중..." -ForegroundColor Blue
    
    $urls = @(
        "http://planit.boramae.club/",
        "http://planit.boramae.club/timetable/",
        "http://planit.boramae.club/planner/",
        "http://planit.boramae.club/community/"
    )
    
    foreach ($url in $urls) {
        try {
            $response = Invoke-WebRequest -Uri $url -UseBasicParsing -ErrorAction Stop
            Write-Host "  ✅ $url - $($response.StatusCode)" -ForegroundColor Green
        } catch {
            Write-Host "  ❌ $url - ERROR" -ForegroundColor Red
        }
    }
} else {
    Write-Host "❌ 배포 중 오류가 발생했습니다." -ForegroundColor Red
}
