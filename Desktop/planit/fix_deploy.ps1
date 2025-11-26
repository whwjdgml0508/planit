# planit 서비스 수정 및 배포 완료 스크립트
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "planit 서비스를 수정하고 배포를 완료합니다..." -ForegroundColor Blue

try {
    $fixCommand = @"
# 홈 디렉토리의 planit 프로젝트로 이동
cd /home/ubuntu/planit

# 최신 코드 가져오기
git pull origin main

# 가상환경 활성화 및 의존성 설치
source venv/bin/activate
pip install -r requirements.txt

# Django 설정
export DJANGO_SETTINGS_MODULE=planit_project.settings.development
python manage.py collectstatic --noinput
python manage.py migrate

# 서비스 파일 수정 - 올바른 경로로 업데이트
sudo tee /etc/systemd/system/planit.service > /dev/null << 'EOF'
[Unit]
Description=Gunicorn instance to serve PlanIt
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/planit
Environment="PATH=/home/ubuntu/planit/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=planit_project.settings.development"
ExecStart=/home/ubuntu/planit/venv/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/planit/planit.sock planit_project.wsgi:application
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

# nginx 설정 업데이트
sudo tee /etc/nginx/sites-available/planit << 'EOF'
server {
    listen 80;
    server_name planit.boramae.club www.planit.boramae.club 35.163.12.109;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/ubuntu/planit;
    }
    
    location /media/ {
        root /home/ubuntu/planit;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/planit/planit.sock;
    }
}
EOF

# 서비스 재시작
sudo systemctl daemon-reload
sudo systemctl enable planit
sudo systemctl restart planit
sudo systemctl restart nginx

# 상태 확인
echo "=== planit 서비스 상태 ==="
sudo systemctl status planit --no-pager
echo "=== nginx 상태 ==="
sudo systemctl status nginx --no-pager
"@
    
    ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP $fixCommand
    
    Write-Host "`n✅ 배포 수정이 완료되었습니다!" -ForegroundColor Green
    Write-Host "🌐 사이트 확인: http://planit.boramae.club/" -ForegroundColor Cyan
    
} catch {
    Write-Host "❌ 오류 발생: $($_.Exception.Message)" -ForegroundColor Red
}
