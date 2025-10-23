# PlanIt 서버 수정 및 Admin 계정 생성
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "서버를 수정하고 admin 계정을 생성합니다..." -ForegroundColor Blue

try {
    $remoteCommand = @"
cd /home/ubuntu/planit

echo "=== 현재 디렉토리 및 파일 확인 ==="
pwd
ls -la

echo "=== 가상환경 확인 ==="
ls -la .venv/bin/ 2>/dev/null || ls -la venv/bin/ 2>/dev/null || echo "가상환경을 찾을 수 없습니다"

echo "=== 시스템 Python으로 Django 확인 ==="
python3 -c "import django; print('Django version:', django.get_version())" 2>/dev/null || echo "Django가 설치되지 않음"

echo "=== pip로 Django 설치 ==="
pip3 install django==4.2.7 djangorestframework mysqlclient pillow crispy-bootstrap5 django-crispy-forms

echo "=== 마이그레이션 실행 ==="
python3 manage.py makemigrations
python3 manage.py migrate

echo "=== Admin 계정 생성 ==="
python3 manage.py shell << 'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()

print("=== 현재 사용자 목록 ===")
for user in User.objects.all():
    print(f"- {user.username} (관리자: {user.is_superuser})")

if User.objects.filter(username='admin').exists():
    print("admin 계정이 이미 존재합니다.")
    admin_user = User.objects.get(username='admin')
    admin_user.is_superuser = True
    admin_user.is_staff = True
    admin_user.save()
    print("admin 계정에 관리자 권한을 부여했습니다.")
else:
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@planit.boramae.club',
        password='planit2024!',
        student_id='0000000',
        first_name='관리자',
        last_name='시스템'
    )
    print("새로운 admin 계정이 생성되었습니다.")

print("Admin 계정 정보:")
admin_user = User.objects.get(username='admin')
print(f"- 사용자명: {admin_user.username}")
print(f"- 이메일: {admin_user.email}")
print(f"- 관리자 권한: {admin_user.is_superuser}")
print(f"- 스태프 권한: {admin_user.is_staff}")
EOF

echo "=== 정적 파일 수집 ==="
python3 manage.py collectstatic --noinput

echo "=== 서버 재시작 ==="
pkill -f python3 || true
pkill -f gunicorn || true
sleep 3

nohup python3 manage.py runserver 0.0.0.0:8000 > server.log 2>&1 &

echo "=== 서버 상태 확인 ==="
sleep 5
ps aux | grep python3 | grep -v grep

echo "✅ 작업 완료!"
echo "🌐 관리자 페이지: http://planit.boramae.club/admin/"
echo "👤 로그인: admin / planit2024!"
"@
    
    ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP $remoteCommand
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✅ 서버 설정 및 Admin 계정 생성이 완료되었습니다!" -ForegroundColor Green
        Write-Host "`n📋 로그인 정보:" -ForegroundColor Blue
        Write-Host "🌐 URL: http://planit.boramae.club/admin/" -ForegroundColor Cyan
        Write-Host "👤 사용자명: admin" -ForegroundColor Cyan
        Write-Host "🔑 비밀번호: planit2024!" -ForegroundColor Cyan
        Write-Host "`n💡 이제 위 정보로 관리자 페이지에 로그인할 수 있습니다." -ForegroundColor Green
        
        # 웹사이트 접속 테스트
        Write-Host "`n🔍 웹사이트 접속 테스트 중..." -ForegroundColor Yellow
        try {
            $response = Invoke-WebRequest -Uri "http://planit.boramae.club" -TimeoutSec 10 -UseBasicParsing
            if ($response.StatusCode -eq 200) {
                Write-Host "✅ 웹사이트가 정상적으로 작동하고 있습니다!" -ForegroundColor Green
            }
        } catch {
            Write-Host "⚠️ 웹사이트 접속에 문제가 있을 수 있습니다. 잠시 후 다시 시도해보세요." -ForegroundColor Yellow
        }
    } else {
        Write-Host "❌ 작업에 실패했습니다." -ForegroundColor Red
    }
    
} catch {
    Write-Host "❌ 오류 발생: $($_.Exception.Message)" -ForegroundColor Red
}
