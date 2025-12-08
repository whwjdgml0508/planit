# Final PlanIt Server Update Script
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "Final server update for PlanIt..." -ForegroundColor Green

# Update the correct server path
Write-Host "Updating server files..." -ForegroundColor Blue
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP @"
cd /var/www/planit/Desktop/planit
source venv/bin/activate
echo "Current working directory: \$(pwd)"
echo "Django version: \$(python -c 'import django; print(django.get_version())')"
python manage.py migrate
python manage.py collectstatic --noinput
"@

# Restart the Django server process
Write-Host "Restarting Django server..." -ForegroundColor Blue
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP @"
sudo pkill -f 'python manage.py runserver'
cd /var/www/planit/Desktop/planit
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=planit_project.settings.development
nohup sudo ./venv/bin/python manage.py runserver 0.0.0.0:80 > server.log 2>&1 &
"@

Write-Host "Server update completed!" -ForegroundColor Green
Write-Host "Please check: http://planit.boramae.club" -ForegroundColor Cyan
Write-Host "Wait a few seconds for the server to fully restart..." -ForegroundColor Yellow
