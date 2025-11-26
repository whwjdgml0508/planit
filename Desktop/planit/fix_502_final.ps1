# 502 오류 해결을 위한 최종 수정 스크립트
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "502 Bad Gateway 오류를 해결합니다..." -ForegroundColor Blue

# 1. /var/www/planit 디렉토리 사용하도록 수정
Write-Host "1. /var/www/planit 디렉토리로 설정 변경..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo cp -r /home/ubuntu/planit/* /var/www/planit/"

# 2. 권한 설정
Write-Host "2. 권한 설정 중..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo chown -R ubuntu:www-data /var/www/planit && sudo chmod -R 755 /var/www/planit"

# 3. 서비스 파일 수정
Write-Host "3. 서비스 파일 수정 중..." -ForegroundColor Yellow
$serviceContent = @'
[Unit]
Description=Gunicorn instance to serve PlanIt
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/var/www/planit
Environment="PATH=/var/www/planit/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=planit_project.settings.development"
ExecStart=/var/www/planit/venv/bin/gunicorn --workers 3 --bind unix:/var/www/planit/planit.sock planit_project.wsgi:application
Restart=on-failure

[Install]
WantedBy=multi-user.target
'@

ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "echo '$serviceContent' | sudo tee /etc/systemd/system/planit.service"

# 4. nginx 설정 수정
Write-Host "4. nginx 설정 수정 중..." -ForegroundColor Yellow
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
        include proxy_params;
        proxy_pass http://unix:/var/www/planit/planit.sock;
    }
}
'@

ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "echo '$nginxContent' | sudo tee /etc/nginx/sites-available/planit"

# 5. Django 설정 및 서비스 재시작
Write-Host "5. Django 설정 및 서비스 재시작..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /var/www/planit && source venv/bin/activate && python manage.py migrate && python manage.py collectstatic --noinput"

ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo systemctl daemon-reload && sudo systemctl restart planit && sudo systemctl restart nginx"

# 6. 상태 확인
Write-Host "6. 최종 상태 확인..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo systemctl status planit && sudo systemctl status nginx"

Write-Host "`n✅ 502 오류 수정이 완료되었습니다!" -ForegroundColor Green
Write-Host "🌐 사이트 확인: http://planit.boramae.club/" -ForegroundColor Cyan
