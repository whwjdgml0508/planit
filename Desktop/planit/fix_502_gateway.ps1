# 502 Bad Gateway 오류 수정 스크립트
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "🔧 502 Bad Gateway 오류 수정 중..." -ForegroundColor Yellow

try {
    # 1단계: 현재 프로세스 상태 확인
    Write-Host "1. 현재 Django 서버 프로세스 확인..." -ForegroundColor Cyan
    ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "ps aux | grep python"
    
    # 2단계: 기존 프로세스 종료
    Write-Host "`n2. 기존 Django 프로세스 종료..." -ForegroundColor Cyan
    ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo pkill -f python; sudo pkill -f gunicorn"
    
    # 3단계: Django 서버 재시작
    Write-Host "`n3. Django 서버 재시작..." -ForegroundColor Cyan
    $startServerCommand = @"
cd /home/ubuntu/planit
source venv/bin/activate
nohup python manage.py runserver 0.0.0.0:8000 > server.log 2>&1 &
sleep 3
echo "Django 서버가 시작되었습니다."
"@
    
    ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP $startServerCommand
    
    # 4단계: 서버 상태 확인
    Write-Host "`n4. 서버 상태 확인..." -ForegroundColor Cyan
    ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "ps aux | grep python | grep -v grep"
    
    # 5단계: 포트 8000 확인
    Write-Host "`n5. 포트 8000 상태 확인..." -ForegroundColor Cyan
    ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "netstat -tlnp | grep :8000"
    
    # 6단계: nginx 재시작
    Write-Host "`n6. nginx 재시작..." -ForegroundColor Cyan
    ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo systemctl restart nginx"
    
    Write-Host "`n✅ 502 오류 수정 완료!" -ForegroundColor Green
    Write-Host "🌐 잠시 후 http://planit.boramae.club/ 를 확인해보세요." -ForegroundColor Cyan
    
} catch {
    Write-Host "❌ 오류 발생: $($_.Exception.Message)" -ForegroundColor Red
}
