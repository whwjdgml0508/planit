# 가상환경을 사용한 Admin 계정 생성
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "가상환경을 사용하여 Admin 계정을 생성합니다..." -ForegroundColor Blue

try {
    # 1. 파일 업로드
    Write-Host "1. Python 스크립트 업로드 중..." -ForegroundColor Yellow
    scp -i $SSH_KEY_PATH "admin_creator.py" "${EC2_USER}@${EC2_IP}:/home/ubuntu/planit/"
    
    # 2. 가상환경에서 스크립트 실행
    Write-Host "2. 가상환경에서 Admin 계정 생성 중..." -ForegroundColor Yellow
    
    $commands = @(
        "cd /home/ubuntu/planit",
        "source venv/bin/activate",
        "python admin_creator.py"
    )
    
    $fullCommand = $commands -join " && "
    ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP $fullCommand
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✅ Admin 계정 생성이 완료되었습니다!" -ForegroundColor Green
        
        # 3. 가상환경에서 서버 재시작
        Write-Host "3. 가상환경에서 서버 재시작 중..." -ForegroundColor Yellow
        
        $serverCommands = @(
            "cd /home/ubuntu/planit",
            "pkill -f python",
            "sleep 2",
            "source venv/bin/activate",
            "nohup python manage.py runserver 0.0.0.0:8000 > server.log 2>&1 &"
        )
        
        $serverCommand = $serverCommands -join " && "
        ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP $serverCommand
        
        Write-Host "`n📋 최종 로그인 정보:" -ForegroundColor Blue
        Write-Host "🌐 URL: http://planit.boramae.club/admin/" -ForegroundColor Cyan
        Write-Host "👤 사용자명: admin" -ForegroundColor Cyan
        Write-Host "🔑 비밀번호: planit2024!" -ForegroundColor Cyan
        
        # 4. 접속 테스트
        Write-Host "`n🔍 웹사이트 접속 테스트 중..." -ForegroundColor Yellow
        Start-Sleep -Seconds 8
        try {
            $response = Invoke-WebRequest -Uri "http://planit.boramae.club" -TimeoutSec 15 -UseBasicParsing
            if ($response.StatusCode -eq 200) {
                Write-Host "✅ 웹사이트가 정상적으로 작동하고 있습니다!" -ForegroundColor Green
                
                # 관리자 페이지 테스트
                try {
                    $adminResponse = Invoke-WebRequest -Uri "http://planit.boramae.club/admin/" -TimeoutSec 10 -UseBasicParsing
                    if ($adminResponse.StatusCode -eq 200) {
                        Write-Host "✅ 관리자 페이지에도 정상적으로 접근할 수 있습니다!" -ForegroundColor Green
                    }
                } catch {
                    Write-Host "⚠️ 관리자 페이지 접근 테스트 실패" -ForegroundColor Yellow
                }
            }
        } catch {
            Write-Host "⚠️ 웹사이트 접근 테스트 실패. 서버가 시작되는 중일 수 있습니다." -ForegroundColor Yellow
        }
        
        Write-Host "`n💡 이제 http://planit.boramae.club/admin/ 에서 admin/planit2024! 로 로그인할 수 있습니다!" -ForegroundColor Green
        Write-Host "💡 만약 로그인이 안 된다면 잠시 후 다시 시도해보세요. 서버가 완전히 시작되는데 시간이 걸릴 수 있습니다." -ForegroundColor Yellow
        
    } else {
        Write-Host "❌ Admin 계정 생성에 실패했습니다." -ForegroundColor Red
    }
    
} catch {
    Write-Host "❌ 오류 발생: $($_.Exception.Message)" -ForegroundColor Red
}
