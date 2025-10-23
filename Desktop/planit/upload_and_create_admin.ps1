# PlanIt Admin 계정 생성 - 파일 업로드 및 실행
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "Admin 계정 생성 스크립트를 서버에 업로드하고 실행합니다..." -ForegroundColor Blue

try {
    # 1. Python 스크립트를 서버에 업로드
    Write-Host "1. 스크립트 파일 업로드 중..." -ForegroundColor Yellow
    scp -i $SSH_KEY_PATH "simple_admin_create.py" "${EC2_USER}@${EC2_IP}:/home/ubuntu/planit/"
    
    if ($LASTEXITCODE -ne 0) {
        throw "파일 업로드 실패"
    }
    
    Write-Host "✅ 파일 업로드 완료" -ForegroundColor Green
    
    # 2. 서버에서 스크립트 실행
    Write-Host "2. 서버에서 admin 계정 생성 중..." -ForegroundColor Yellow
    
    $remoteCommand = @"
cd /home/ubuntu/planit
python3 simple_admin_create.py
"@
    
    ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP $remoteCommand
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✅ Admin 계정 생성이 완료되었습니다!" -ForegroundColor Green
        Write-Host "`n📋 로그인 정보:" -ForegroundColor Blue
        Write-Host "🌐 URL: http://planit.boramae.club/admin/" -ForegroundColor Cyan
        Write-Host "👤 사용자명: admin" -ForegroundColor Cyan
        Write-Host "🔑 비밀번호: planit2024!" -ForegroundColor Cyan
        Write-Host "`n💡 이제 위 정보로 관리자 페이지에 로그인할 수 있습니다." -ForegroundColor Green
    } else {
        Write-Host "❌ Admin 계정 생성에 실패했습니다." -ForegroundColor Red
    }
    
} catch {
    Write-Host "❌ 오류 발생: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "SSH 키 파일 경로를 확인해주세요: $SSH_KEY_PATH" -ForegroundColor Yellow
}
