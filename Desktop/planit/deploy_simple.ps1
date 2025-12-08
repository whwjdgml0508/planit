# 간단한 PlanIt 배포 스크립트

$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "c:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "🚀 PlanIt 서버 배포 시작..." -ForegroundColor Green

# SSH 명령들을 개별적으로 실행
Write-Host "📥 Git pull 실행 중..." -ForegroundColor Blue
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /var/www/planit && git pull origin main"

Write-Host "🗄️ 데이터베이스 마이그레이션 실행 중..." -ForegroundColor Blue
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /var/www/planit && source venv/bin/activate && python manage.py migrate"

Write-Host "📁 정적 파일 수집 중..." -ForegroundColor Blue
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /var/www/planit && source venv/bin/activate && python manage.py collectstatic --noinput"

Write-Host "🔄 서버 재시작 중..." -ForegroundColor Blue
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo systemctl restart planit && sudo systemctl restart nginx"

Write-Host "✅ 배포 완료!" -ForegroundColor Green
Write-Host "🌐 웹사이트 확인: http://planit.boramae.club" -ForegroundColor Cyan
