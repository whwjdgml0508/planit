# 502 오류 디버깅 스크립트
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "502 오류를 디버깅합니다..." -ForegroundColor Blue

# 1. 서비스 로그 확인
Write-Host "1. planit 서비스 로그 확인..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo journalctl -u planit -n 20"

# 2. nginx 로그 확인
Write-Host "2. nginx 오류 로그 확인..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo tail -20 /var/log/nginx/error.log"

# 3. 소켓 파일 확인
Write-Host "3. 소켓 파일 상태 확인..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "ls -la /var/www/planit/planit.sock"

# 4. gunicorn을 직접 테스트
Write-Host "4. gunicorn 직접 테스트..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /var/www/planit && source venv/bin/activate && python -c 'import planit_project.wsgi'"
