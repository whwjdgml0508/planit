# 502 Bad Gateway 오류 해결 스크립트
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "502 Bad Gateway 오류를 해결합니다..." -ForegroundColor Red

# 1. 서버 상태 진단
Write-Host "`n1. 서버 상태 진단 중..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP @"
echo "=== 실행 중인 Python 프로세스 확인 ==="
ps aux | grep python | grep -v grep

echo -e "\n=== 포트 8000 상태 확인 ==="
netstat -tlnp | grep :8000 || echo "포트 8000에서 실행 중인 서비스가 없습니다"

echo -e "\n=== nginx 상태 확인 ==="
sudo systemctl status nginx --no-pager

echo -e "\n=== nginx 오류 로그 확인 ==="
sudo tail -10 /var/log/nginx/error.log

echo -e "\n=== 디스크 공간 확인 ==="
df -h

echo -e "\n=== 메모리 사용량 확인 ==="
free -h
"@

# 2. Django 서버 재시작
Write-Host "`n2. Django 서버 재시작 중..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP @"
cd /home/ubuntu/planit

echo "기존 Python 프로세스 종료..."
pkill -f python || true
pkill -f gunicorn || true
sleep 3

echo "가상환경에서 Django 서버 시작..."
source venv/bin/activate
nohup python manage.py runserver 0.0.0.0:8000 > server.log 2>&1 &

echo "서버 시작 대기..."
sleep 5

echo "새로운 프로세스 확인..."
ps aux | grep python | grep runserver
"@

# 3. nginx 재시작
Write-Host "`n3. nginx 재시작 중..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP @"
echo "nginx 재시작..."
sudo systemctl restart nginx

echo "nginx 상태 확인..."
sudo systemctl status nginx --no-pager
"@

Write-Host "`n✅ 502 오류 해결 작업 완료!" -ForegroundColor Green
Write-Host "잠시 후 웹사이트에 다시 접속해보세요." -ForegroundColor Blue

# 4. 접속 테스트
Write-Host "`n4. 웹사이트 접속 테스트 중..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

try {
    $response = Invoke-WebRequest -Uri "http://planit.boramae.club" -TimeoutSec 20 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ 웹사이트가 정상적으로 작동합니다!" -ForegroundColor Green
        
        # 관리자 페이지 테스트
        try {
            $adminResponse = Invoke-WebRequest -Uri "http://planit.boramae.club/admin/" -TimeoutSec 15 -UseBasicParsing
            if ($adminResponse.StatusCode -eq 200) {
                Write-Host "✅ 관리자 페이지도 정상 작동합니다!" -ForegroundColor Green
            }
        } catch {
            Write-Host "⚠️ 관리자 페이지는 아직 준비 중일 수 있습니다." -ForegroundColor Yellow
        }
    }
} catch {
    Write-Host "❌ 여전히 접속 문제가 있습니다. 추가 진단이 필요합니다." -ForegroundColor Red
}

Write-Host "`n📋 관리자 로그인 정보:" -ForegroundColor Blue
Write-Host "🌐 URL: http://planit.boramae.club/admin/" -ForegroundColor Cyan
Write-Host "👤 사용자명: admin" -ForegroundColor Cyan
Write-Host "🔑 비밀번호: planit2024!" -ForegroundColor Cyan
