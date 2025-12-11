# PlanIt Media Files 404 오류 해결 스크립트

Write-Host "=== PlanIt Media Files 404 오류 진단 및 해결 ===" -ForegroundColor Cyan
Write-Host ""

# SSH 접속 정보
$sshKey = "~/.ssh/ec2-kafa-2-key.pem"
$server = "ubuntu@35.163.12.109"

Write-Host "1. 서버 접속 및 media 디렉토리 확인..." -ForegroundColor Yellow
ssh -i $sshKey $server @"
echo '=== Media 디렉토리 구조 확인 ==='
ls -la /home/ubuntu/planit/media/ 2>/dev/null || echo 'media 디렉토리 없음'
ls -la /var/www/planit/media/ 2>/dev/null || echo '/var/www/planit/media 디렉토리 없음'
echo ''

echo '=== profiles 디렉토리 확인 ==='
ls -la /home/ubuntu/planit/media/profiles/ 2>/dev/null || echo 'profiles 디렉토리 없음'
ls -la /var/www/planit/media/profiles/ 2>/dev/null || echo '/var/www/planit/media/profiles 디렉토리 없음'
echo ''

echo '=== Django 프로젝트 위치 확인 ==='
cd /home/ubuntu/planit
python3 manage.py shell << 'PYEOF'
from django.conf import settings
print(f'MEDIA_ROOT: {settings.MEDIA_ROOT}')
print(f'MEDIA_URL: {settings.MEDIA_URL}')
PYEOF
echo ''

echo '=== 실제 업로드된 파일 찾기 ==='
find /home/ubuntu/planit -name '*0I9S19B.JPG' 2>/dev/null
find /var/www/planit -name '*0I9S19B.JPG' 2>/dev/null
echo ''
"@

Write-Host ""
Write-Host "2. media 디렉토리 생성 및 파일 복사..." -ForegroundColor Yellow
ssh -i $sshKey $server @"
# /var/www/planit/media 디렉토리 생성
sudo mkdir -p /var/www/planit/media/profiles
sudo mkdir -p /var/www/planit/media/posts
sudo mkdir -p /var/www/planit/media/comments

# /home/ubuntu/planit/media에서 파일 복사
if [ -d '/home/ubuntu/planit/media' ]; then
    echo '기존 media 파일 복사 중...'
    sudo cp -r /home/ubuntu/planit/media/* /var/www/planit/media/ 2>/dev/null || true
fi

# 권한 설정
sudo chown -R www-data:www-data /var/www/planit/media
sudo chmod -R 755 /var/www/planit/media

echo '=== 복사 후 확인 ==='
ls -la /var/www/planit/media/
ls -la /var/www/planit/media/profiles/ 2>/dev/null || echo 'profiles 디렉토리 비어있음'
"@

Write-Host ""
Write-Host "3. nginx 설정 확인 및 재시작..." -ForegroundColor Yellow
ssh -i $sshKey $server @"
echo '=== nginx 설정 확인 ==='
sudo nginx -t

echo ''
echo '=== nginx 재시작 ==='
sudo systemctl restart nginx
sudo systemctl status nginx --no-pager -l
"@

Write-Host ""
Write-Host "4. 테스트..." -ForegroundColor Yellow
Write-Host "브라우저에서 다음 URL 접속 테스트:" -ForegroundColor Green
Write-Host "http://planit.boramae.club/media/profiles/1-송정희_0I9S19B.JPG" -ForegroundColor White

Write-Host ""
Write-Host "=== 완료 ===" -ForegroundColor Cyan
