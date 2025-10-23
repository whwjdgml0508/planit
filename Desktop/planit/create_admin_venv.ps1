# 가상환경을 사용한 Admin 계정 생성
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "가상환경을 사용하여 Admin 계정을 생성합니다..." -ForegroundColor Blue

try {
    $remoteCommand = @"
cd /home/ubuntu/planit

echo "=== 가상환경 활성화 ==="
source venv/bin/activate

echo "=== setuptools 설치 (가상환경) ==="
pip install setuptools

echo "=== Django 설정 확인 ==="
export DJANGO_SETTINGS_MODULE=planit_project.settings.development
python -c "import django; django.setup(); print('Django 설정 완료')"

echo "=== 마이그레이션 실행 ==="
python manage.py makemigrations
python manage.py migrate

echo "=== Admin 계정 생성 ==="
python -c "
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
python manage.py collectstatic --noinput

echo "=== 서버 재시작 ==="
pkill -f python || true
sleep 3
nohup python manage.py runserver 0.0.0.0:8000 > server.log 2>&1 &

echo "=== 서버 상태 확인 ==="
sleep 5
ps aux | grep python | grep runserver

echo "✅ 모든 작업이 완료되었습니다!"
echo "🌐 관리자 페이지: http://planit.boramae.club/admin/"
echo "👤 로그인: admin / planit2024!"
"@
    
    ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP $remoteCommand
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✅ Admin 계정이 성공적으로 생성되었습니다!" -ForegroundColor Green
        
        # 로그인 테스트
        Write-Host "`n🔍 로그인 기능 테스트 중..." -ForegroundColor Yellow
        try {
            $loginUrl = "http://planit.boramae.club/admin/login/"
            $response = Invoke-WebRequest -Uri $loginUrl -TimeoutSec 10 -UseBasicParsing
            if ($response.StatusCode -eq 200) {
                Write-Host "✅ 관리자 로그인 페이지에 접근 가능합니다!" -ForegroundColor Green
            }
        } catch {
            Write-Host "⚠️ 로그인 페이지 접근 테스트 실패" -ForegroundColor Yellow
        }
        
        Write-Host "`n📋 최종 로그인 정보:" -ForegroundColor Blue
        Write-Host "🌐 URL: http://planit.boramae.club/admin/" -ForegroundColor Cyan
        Write-Host "👤 사용자명: admin" -ForegroundColor Cyan
        Write-Host "🔑 비밀번호: planit2024!" -ForegroundColor Cyan
        Write-Host "`n💡 이제 위 정보로 관리자 페이지에 로그인할 수 있습니다!" -ForegroundColor Green
    } else {
        Write-Host "❌ Admin 계정 생성에 실패했습니다." -ForegroundColor Red
    }
    
} catch {
    Write-Host "❌ 오류 발생: $($_.Exception.Message)" -ForegroundColor Red
}
