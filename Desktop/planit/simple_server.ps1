# 간단한 Django 개발 서버로 테스트
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "Django 개발 서버로 테스트합니다..." -ForegroundColor Blue

# 1. planit 서비스 중지
Write-Host "1. planit 서비스 중지..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo systemctl stop planit"

# 2. nginx 설정을 개발 서버용으로 변경
Write-Host "2. nginx 설정을 개발 서버용으로 변경..." -ForegroundColor Yellow
$nginxContent = @'
server {
    listen 80;
    server_name planit.boramae.club www.planit.boramae.club 35.163.12.109;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /var/www/planit;
    }
    
    location /media/ {
        root /var/www/planit;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
'@

ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "echo '$nginxContent' | sudo tee /etc/nginx/sites-available/planit"

# 3. nginx 재시작
Write-Host "3. nginx 재시작..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo systemctl restart nginx"

# 4. Django 개발 서버 시작
Write-Host "4. Django 개발 서버 시작..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /var/www/planit && nohup python manage.py runserver 0.0.0.0:8000 > server.log 2>&1 &"

Write-Host "`n✅ 개발 서버가 시작되었습니다!" -ForegroundColor Green
Write-Host "🌐 사이트 확인: http://planit.boramae.club/" -ForegroundColor Cyan
Write-Host "📋 서버 로그 확인: ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP 'tail -f /var/www/planit/server.log'" -ForegroundColor Yellow
