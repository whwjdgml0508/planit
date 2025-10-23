# 간단한 SSH 명령으로 Admin 계정 생성
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "Python 스크립트를 업로드하고 실행합니다..." -ForegroundColor Blue

try {
    # 1. 파일 업로드
    Write-Host "1. Python 스크립트 업로드 중..." -ForegroundColor Yellow
    scp -i $SSH_KEY_PATH "admin_creator.py" "${EC2_USER}@${EC2_IP}:/home/ubuntu/planit/"
    
    # 2. 스크립트 실행
    Write-Host "2. Admin 계정 생성 스크립트 실행 중..." -ForegroundColor Yellow
    ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /home/ubuntu/planit && python3 admin_creator.py"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✅ Admin 계정 생성이 완료되었습니다!" -ForegroundColor Green
        
        # 3. 서버 재시작
        Write-Host "3. 서버 재시작 중..." -ForegroundColor Yellow
        ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /home/ubuntu/planit && pkill -f python3 && sleep 2 && nohup python3 manage.py runserver 0.0.0.0:8000 > server.log 2>&1 &"
        
        Write-Host "`n📋 최종 로그인 정보:" -ForegroundColor Blue
        Write-Host "🌐 URL: http://planit.boramae.club/admin/" -ForegroundColor Cyan
        Write-Host "👤 사용자명: admin" -ForegroundColor Cyan
        Write-Host "🔑 비밀번호: planit2024!" -ForegroundColor Cyan
        
        # 4. 접속 테스트
        Write-Host "`n🔍 웹사이트 접속 테스트 중..." -ForegroundColor Yellow
        Start-Sleep -Seconds 5
        try {
            $response = Invoke-WebRequest -Uri "http://planit.boramae.club/admin/" -TimeoutSec 15 -UseBasicParsing
            if ($response.StatusCode -eq 200) {
                Write-Host "✅ 관리자 페이지에 정상적으로 접근할 수 있습니다!" -ForegroundColor Green
            }
        } catch {
            Write-Host "⚠️ 관리자 페이지 접근 테스트 실패. 서버가 시작되는 중일 수 있습니다." -ForegroundColor Yellow
        }
        
        Write-Host "`n💡 이제 http://planit.boramae.club/admin/ 에서 admin/planit2024! 로 로그인할 수 있습니다!" -ForegroundColor Green
    } else {
        Write-Host "❌ Admin 계정 생성에 실패했습니다." -ForegroundColor Red
    }
    
} catch {
    Write-Host "❌ 오류 발생: $($_.Exception.Message)" -ForegroundColor Red
}
