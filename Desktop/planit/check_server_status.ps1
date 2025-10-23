# PlanIt 서버 상태 확인 스크립트
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "서버 상태를 확인합니다..." -ForegroundColor Blue

try {
    $remoteCommand = @"
echo "=== 서버 기본 정보 ==="
whoami
pwd
ls -la /home/ubuntu/

echo -e "\n=== PlanIt 프로젝트 디렉토리 ==="
ls -la /home/ubuntu/planit/

echo -e "\n=== Python 환경 ==="
python3 --version
which python3

echo -e "\n=== 가상환경 확인 ==="
ls -la /home/ubuntu/planit/planit/venv/ 2>/dev/null || echo "가상환경이 없습니다"

echo -e "\n=== Django 프로젝트 파일 확인 ==="
ls -la /home/ubuntu/planit/manage.py 2>/dev/null || echo "manage.py가 없습니다"

echo -e "\n=== 설치된 패키지 확인 (시스템) ==="
pip3 list | grep -i django || echo "Django가 시스템에 설치되지 않음"

echo -e "\n=== requirements.txt 확인 ==="
cat /home/ubuntu/planit/requirements.txt 2>/dev/null || echo "requirements.txt가 없습니다"

echo -e "\n=== 실행 중인 프로세스 ==="
ps aux | grep python | grep -v grep || echo "실행 중인 Python 프로세스가 없습니다"

echo -e "\n=== 포트 8000 확인 ==="
netstat -tlnp | grep :8000 || echo "포트 8000에서 실행 중인 서비스가 없습니다"
"@
    
    ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP $remoteCommand
    
} catch {
    Write-Host "❌ 서버 접속 실패: $($_.Exception.Message)" -ForegroundColor Red
}
