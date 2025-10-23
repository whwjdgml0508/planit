# 최종 Admin 계정 설정
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "최종 Admin 계정 설정을 진행합니다..." -ForegroundColor Blue

try {
    $remoteCommand = @"
cd /home/ubuntu/planit

echo "=== setuptools 설치 ==="
pip3 install setuptools

echo "=== Django 설정 확인 ==="
export DJANGO_SETTINGS_MODULE=planit_project.settings.development
python3 -c "import django; django.setup(); print('Django 설정 완료')"

echo "=== 마이그레이션 실행 ==="
python3 manage.py makemigrations
python3 manage.py migrate

echo "=== Admin 계정 생성 ==="
python3 -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.development')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

if User.objects.filter(username='admin').exists():
    print('admin 계정이 이미 존재합니다.')
    admin_user = User.objects.get(username='admin')
    admin_user.is_superuser = True
    admin_user.is_staff = True
    admin_user.save()
    print('admin 계정에 관리자 권한을 부여했습니다.')
else:
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@planit.boramae.club',
        password='planit2024!',
        student_id='0000000',
        first_name='관리자',
        last_name='시스템'
    )
    print('새로운 admin 계정이 생성되었습니다.')

print('Admin 계정 정보:')
admin_user = User.objects.get(username='admin')
print(f'- 사용자명: {admin_user.username}')
print(f'- 이메일: {admin_user.email}')
print(f'- 관리자 권한: {admin_user.is_superuser}')
print(f'- 스태프 권한: {admin_user.is_staff}')
"

echo "=== 정적 파일 수집 ==="
python3 manage.py collectstatic --noinput

echo "=== 서버 재시작 ==="
pkill -f python3 || true
sleep 3
nohup python3 manage.py runserver 0.0.0.0:8000 > server.log 2>&1 &

echo "=== 서버 상태 확인 ==="
sleep 5
ps aux | grep python3 | grep runserver

echo "✅ 모든 작업이 완료되었습니다!"
echo "🌐 관리자 페이지: http://planit.boramae.club/admin/"
echo "👤 로그인: admin / planit2024!"
"@
    
    ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP $remoteCommand
    
    Write-Host "`n✅ Admin 계정 설정이 완료되었습니다!" -ForegroundColor Green
    Write-Host "`n📋 로그인 정보:" -ForegroundColor Blue
    Write-Host "🌐 URL: http://planit.boramae.club/admin/" -ForegroundColor Cyan
    Write-Host "👤 사용자명: admin" -ForegroundColor Cyan
    Write-Host "🔑 비밀번호: planit2024!" -ForegroundColor Cyan
    
    # 웹사이트 접속 테스트
    Write-Host "`n🔍 웹사이트 접속 테스트 중..." -ForegroundColor Yellow
    Start-Sleep -Seconds 3
    try {
        $response = Invoke-WebRequest -Uri "http://planit.boramae.club" -TimeoutSec 15 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ 웹사이트가 정상적으로 작동하고 있습니다!" -ForegroundColor Green
        }
    } catch {
        Write-Host "⚠️ 웹사이트 접속 테스트 실패. 서버가 시작되는 중일 수 있습니다." -ForegroundColor Yellow
    }
    
    Write-Host "`n💡 이제 http://planit.boramae.club/admin/ 에서 admin/planit2024! 로 로그인할 수 있습니다." -ForegroundColor Green
    
} catch {
    Write-Host "❌ 오류 발생: $($_.Exception.Message)" -ForegroundColor Red
}
