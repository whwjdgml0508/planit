# PlanIt 서버 경로 수정 및 배포 스크립트
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "서버 경로 수정 및 배포 시작..." -ForegroundColor Green

# 1. 올바른 경로 확인 및 manage.py 찾기
Write-Host "manage.py 파일 위치 확인 중..." -ForegroundColor Blue
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "find /home/ubuntu -name 'manage.py' -type f 2>/dev/null"

# 2. 프로젝트 구조 확인
Write-Host "프로젝트 구조 확인 중..." -ForegroundColor Blue
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "ls -la /home/ubuntu/planit/"

# 3. Git pull 실행 (올바른 경로에서)
Write-Host "Git pull 실행 중..." -ForegroundColor Blue
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /home/ubuntu/planit; git pull origin main"

# 4. 가상환경 활성화 및 Django 명령 실행
Write-Host "가상환경에서 Django 명령 실행 중..." -ForegroundColor Blue
$djangoCommands = @"
cd /home/ubuntu/planit
source venv/bin/activate
echo "현재 디렉토리: \$(pwd)"
echo "Python 경로: \$(which python)"
echo "Django 버전: \$(python -c 'import django; print(django.get_version())')"
ls -la manage.py
python manage.py migrate
python manage.py collectstatic --noinput
"@

ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP $djangoCommands

# 5. 서버 재시작
Write-Host "서버 재시작 중..." -ForegroundColor Blue
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo systemctl restart planit 2>/dev/null; echo 'planit 서비스 재시작 시도'"
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo systemctl restart nginx 2>/dev/null; echo 'nginx 재시작 시도'"

# 6. 서버 상태 확인
Write-Host "서버 상태 확인 중..." -ForegroundColor Blue
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "ps aux | grep python | grep -v grep"

Write-Host "작업 완료!" -ForegroundColor Green
Write-Host "웹사이트 확인: http://planit.boramae.club" -ForegroundColor Cyan
