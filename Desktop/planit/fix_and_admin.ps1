# setuptools 설치 후 Admin 계정 생성
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "setuptools를 설치하고 Admin 계정을 생성합니다..." -ForegroundColor Blue

# 1. setuptools 설치
Write-Host "1. setuptools 설치 중..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /home/ubuntu/planit && source venv/bin/activate && pip install setuptools"

# 2. Admin 계정 생성 스크립트 실행
Write-Host "2. Admin 계정 생성 중..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /home/ubuntu/planit && source venv/bin/activate && python admin_creator.py"

# 3. 서버 재시작
Write-Host "3. 서버 재시작 중..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /home/ubuntu/planit && pkill -f python || true && sleep 3 && source venv/bin/activate && nohup python manage.py runserver 0.0.0.0:8000 > server.log 2>&1 &"

Write-Host "`n✅ 모든 작업이 완료되었습니다!" -ForegroundColor Green
Write-Host "`n📋 로그인 정보:" -ForegroundColor Blue
Write-Host "🌐 URL: http://planit.boramae.club/admin/" -ForegroundColor Cyan
Write-Host "👤 사용자명: admin" -ForegroundColor Cyan
Write-Host "🔑 비밀번호: planit2024!" -ForegroundColor Cyan

# 4. 잠시 대기 후 접속 테스트
Write-Host "`n🔍 서버 시작 대기 중..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host "웹사이트 접속 테스트 중..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://planit.boramae.club" -TimeoutSec 20 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ 웹사이트가 정상적으로 작동하고 있습니다!" -ForegroundColor Green
        
        # 관리자 페이지 테스트
        try {
            $adminResponse = Invoke-WebRequest -Uri "http://planit.boramae.club/admin/" -TimeoutSec 15 -UseBasicParsing
            if ($adminResponse.StatusCode -eq 200) {
                Write-Host "✅ 관리자 페이지에도 정상적으로 접근할 수 있습니다!" -ForegroundColor Green
            }
        } catch {
            Write-Host "⚠️ 관리자 페이지는 아직 준비 중일 수 있습니다." -ForegroundColor Yellow
        }
    }
} catch {
    Write-Host "⚠️ 웹사이트가 아직 시작되지 않았을 수 있습니다. 잠시 후 다시 시도해보세요." -ForegroundColor Yellow
}

Write-Host "`n💡 이제 http://planit.boramae.club/admin/ 에서 admin/planit2024! 로 로그인할 수 있습니다!" -ForegroundColor Green
