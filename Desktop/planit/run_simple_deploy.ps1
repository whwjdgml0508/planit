# 서버의 simple-deploy.sh 스크립트 실행
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "서버의 배포 스크립트를 실행합니다..." -ForegroundColor Blue

try {
    $remoteCommand = @"
cd /home/ubuntu/planit
chmod +x simple-deploy.sh
./simple-deploy.sh
"@
    
    ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP $remoteCommand
    
    Write-Host "`n배포 스크립트 실행 완료. 이제 admin 계정을 생성합니다..." -ForegroundColor Yellow
    
    # admin 계정 생성
    $adminCommand = @"
cd /home/ubuntu/planit
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@planit.boramae.club', 'planit2024!', student_id='0000000', first_name='관리자', last_name='시스템') if not User.objects.filter(username='admin').exists() else print('Admin already exists')" | python3 manage.py shell
"@
    
    ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP $adminCommand
    
    Write-Host "`n✅ 작업이 완료되었습니다!" -ForegroundColor Green
    Write-Host "`n📋 로그인 정보:" -ForegroundColor Blue
    Write-Host "🌐 URL: http://planit.boramae.club/admin/" -ForegroundColor Cyan
    Write-Host "👤 사용자명: admin" -ForegroundColor Cyan
    Write-Host "🔑 비밀번호: planit2024!" -ForegroundColor Cyan
    
} catch {
    Write-Host "❌ 오류 발생: $($_.Exception.Message)" -ForegroundColor Red
}
