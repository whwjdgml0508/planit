# 최종 Admin 계정 생성 스크립트
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "Admin 계정을 생성합니다..." -ForegroundColor Blue

# 1. 파일 업로드
Write-Host "1. Python 스크립트 업로드 중..." -ForegroundColor Yellow
scp -i $SSH_KEY_PATH "admin_creator.py" "${EC2_USER}@${EC2_IP}:/home/ubuntu/planit/"

# 2. 가상환경에서 스크립트 실행
Write-Host "2. 가상환경에서 Admin 계정 생성 중..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /home/ubuntu/planit && source venv/bin/activate && python admin_creator.py"

# 3. 서버 재시작
Write-Host "3. 서버 재시작 중..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /home/ubuntu/planit && pkill -f python && sleep 2 && source venv/bin/activate && nohup python manage.py runserver 0.0.0.0:8000 > server.log 2>&1 &"

Write-Host "`n✅ 작업이 완료되었습니다!" -ForegroundColor Green
Write-Host "`n📋 로그인 정보:" -ForegroundColor Blue
Write-Host "🌐 URL: http://planit.boramae.club/admin/" -ForegroundColor Cyan
Write-Host "👤 사용자명: admin" -ForegroundColor Cyan
Write-Host "🔑 비밀번호: planit2024!" -ForegroundColor Cyan

# 4. 접속 테스트
Write-Host "`n🔍 웹사이트 접속 테스트 중..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

$testUrl = "http://planit.boramae.club"
$adminUrl = "http://planit.boramae.club/admin/"

Write-Host "메인 페이지 테스트..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri $testUrl -TimeoutSec 15 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ 메인 페이지가 정상적으로 작동합니다!" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️ 메인 페이지 접근 실패" -ForegroundColor Yellow
}

Write-Host "관리자 페이지 테스트..." -ForegroundColor Yellow
try {
    $adminResponse = Invoke-WebRequest -Uri $adminUrl -TimeoutSec 10 -UseBasicParsing
    if ($adminResponse.StatusCode -eq 200) {
        Write-Host "✅ 관리자 페이지에 정상적으로 접근할 수 있습니다!" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️ 관리자 페이지 접근 실패" -ForegroundColor Yellow
}

Write-Host "`n💡 이제 http://planit.boramae.club/admin/ 에서 admin/planit2024! 로 로그인할 수 있습니다!" -ForegroundColor Green
Write-Host "💡 만약 로그인이 안 된다면 잠시 후 다시 시도해보세요." -ForegroundColor Yellow
