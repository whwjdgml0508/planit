# Manual PlanIt Server Update Script
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "Manual server update for PlanIt..." -ForegroundColor Green

# Execute commands one by one
Write-Host "1. Navigating to correct directory..." -ForegroundColor Blue
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /var/www/planit/Desktop/planit && pwd"

Write-Host "2. Activating virtual environment and running migrate..." -ForegroundColor Blue
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /var/www/planit/Desktop/planit && source venv/bin/activate && python manage.py migrate"

Write-Host "3. Collecting static files..." -ForegroundColor Blue
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /var/www/planit/Desktop/planit && source venv/bin/activate && python manage.py collectstatic --noinput"

Write-Host "4. Killing existing Django processes..." -ForegroundColor Blue
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo pkill -f 'python manage.py runserver'"

Write-Host "5. Starting Django server..." -ForegroundColor Blue
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /var/www/planit/Desktop/planit && source venv/bin/activate && export DJANGO_SETTINGS_MODULE=planit_project.settings.development && nohup sudo ./venv/bin/python manage.py runserver 0.0.0.0:80 > server.log 2>&1 &"

Write-Host "6. Checking server status..." -ForegroundColor Blue
Start-Sleep -Seconds 3
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "ps aux | grep 'python manage.py runserver' | grep -v grep"

Write-Host "Server update completed!" -ForegroundColor Green
Write-Host "Please check: http://planit.boramae.club" -ForegroundColor Cyan
