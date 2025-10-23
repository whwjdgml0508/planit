# PlanIt Admin 계정 생성 스크립트 (PowerShell용)
# EC2 서버에 SSH로 접속하여 admin 계정을 생성합니다.

$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "EC2 서버에 접속하여 admin 계정을 생성합니다..." -ForegroundColor Blue

# SSH 명령어 구성
$sshCommand = @"
cd /home/ubuntu/planit

# 가상환경 활성화
source /home/ubuntu/planit/planit/venv/bin/activate

echo "🔍 현재 사용자 목록 확인 중..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
print('=== 현재 등록된 사용자 ===')
for user in User.objects.all():
    print(f'- {user.username} (관리자: {user.is_superuser})')
print(f'총 {User.objects.count()}명의 사용자가 등록되어 있습니다.')
"

echo "👤 admin 계정 생성 중..."
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
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@planit.boramae.club',
        password='planit2024!',
        student_id='0000000',
        first_name='관리자',
        last_name='시스템'
    )
    print('새로운 admin 계정이 생성되었습니다.')
    print('사용자명: admin')
    print('비밀번호: planit2024!')
    print('이메일: admin@planit.boramae.club')
"

echo "🔍 admin 계정 생성 후 확인..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
try:
    admin_user = User.objects.get(username='admin')
    print(f'✅ admin 계정 확인됨')
    print(f'   - 사용자명: {admin_user.username}')
    print(f'   - 이메일: {admin_user.email}')
    print(f'   - 관리자 권한: {admin_user.is_superuser}')
    print(f'   - 스태프 권한: {admin_user.is_staff}')
    print(f'   - 학번: {admin_user.student_id}')
except User.DoesNotExist:
    print('❌ admin 계정을 찾을 수 없습니다.')
"

echo "🔄 서버 재시작 중..."
pkill -f python || true
pkill -f gunicorn || true
sleep 2
nohup python manage.py runserver 0.0.0.0:8000 > server.log 2>&1 &

echo "✅ 작업 완료!"
echo "📊 서버 로그 확인: tail -f /home/ubuntu/planit/server.log"
echo "🌐 관리자 페이지: http://planit.boramae.club/admin/"
echo "👤 로그인 정보:"
echo "   - 사용자명: admin"
echo "   - 비밀번호: planit2024!"
"@

try {
    # SSH 접속 및 명령 실행
    ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP $sshCommand
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Admin 계정 생성이 완료되었습니다!" -ForegroundColor Green
        Write-Host "관리자 페이지에 접속하세요:" -ForegroundColor Blue
        Write-Host "- URL: http://planit.boramae.club/admin/" -ForegroundColor Blue
        Write-Host "- 사용자명: admin" -ForegroundColor Blue
        Write-Host "- 비밀번호: planit2024!" -ForegroundColor Blue
    } else {
        Write-Host "❌ Admin 계정 생성에 실패했습니다." -ForegroundColor Red
    }
} catch {
    Write-Host "❌ SSH 접속에 실패했습니다: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "SSH 키 파일 경로를 확인해주세요: $SSH_KEY_PATH" -ForegroundColor Yellow
}
