# PlanIt Admin 계정 생성 - 가상환경 사용
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "가상환경을 활성화하고 admin 계정을 생성합니다..." -ForegroundColor Blue

try {
    $remoteCommand = @"
cd /home/ubuntu/planit

echo "=== 가상환경 활성화 ==="
source .venv/bin/activate

echo "=== Python 환경 확인 ==="
which python
python --version

echo "=== Django 설치 확인 ==="
python -c "import django; print('Django version:', django.get_version())"

echo "=== 현재 사용자 목록 확인 ==="
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
print('=== 현재 등록된 사용자 ===')
for user in User.objects.all():
    print(f'- {user.username} (관리자: {user.is_superuser})')
print(f'총 {User.objects.count()}명의 사용자가 등록되어 있습니다.')
"

echo "=== Admin 계정 생성 ==="
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()

# admin 계정이 이미 있는지 확인
if User.objects.filter(username='admin').exists():
    print('admin 계정이 이미 존재합니다.')
    admin_user = User.objects.get(username='admin')
    if not admin_user.is_superuser:
        admin_user.is_superuser = True
        admin_user.is_staff = True
        admin_user.save()
        print('기존 admin 계정에 관리자 권한을 부여했습니다.')
    else:
        print('admin 계정은 이미 관리자 권한을 가지고 있습니다.')
else:
    # 새로운 admin 계정 생성
    try:
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@planit.boramae.club',
            password='planit2024!',
            student_id='0000000',
            first_name='관리자',
            last_name='시스템'
        )
        print('✅ 새로운 admin 계정이 생성되었습니다!')
        print('사용자명: admin')
        print('비밀번호: planit2024!')
        print('이메일: admin@planit.boramae.club')
    except Exception as e:
        print(f'❌ admin 계정 생성 실패: {e}')
"

echo "=== Admin 계정 최종 확인 ==="
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
try:
    admin_user = User.objects.get(username='admin')
    print('✅ Admin 계정 확인됨:')
    print(f'   - 사용자명: {admin_user.username}')
    print(f'   - 이메일: {admin_user.email}')
    print(f'   - 관리자 권한: {admin_user.is_superuser}')
    print(f'   - 스태프 권한: {admin_user.is_staff}')
    print(f'   - 학번: {admin_user.student_id}')
except User.DoesNotExist:
    print('❌ admin 계정을 찾을 수 없습니다.')
"

echo "=== 서버 재시작 ==="
pkill -f python || true
pkill -f gunicorn || true
sleep 2

# 가상환경에서 서버 실행
source .venv/bin/activate
nohup python manage.py runserver 0.0.0.0:8000 > server.log 2>&1 &

echo "✅ 작업 완료!"
echo "🌐 관리자 페이지: http://planit.boramae.club/admin/"
echo "👤 로그인 정보: admin / planit2024!"
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
}
