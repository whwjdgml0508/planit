# PlanIt Server Update Script
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "Starting PlanIt server update..." -ForegroundColor Green

# 1. Find manage.py location
Write-Host "Finding manage.py location..." -ForegroundColor Blue
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "find /home/ubuntu -name 'manage.py' -type f 2>/dev/null"

# 2. Check project structure
Write-Host "Checking project structure..." -ForegroundColor Blue
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "ls -la /home/ubuntu/planit/"

# 3. Git pull
Write-Host "Executing git pull..." -ForegroundColor Blue
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /home/ubuntu/planit; git pull origin main"

# 4. Django commands in virtual environment
Write-Host "Running Django commands..." -ForegroundColor Blue
$djangoCommands = @"
cd /home/ubuntu/planit
source venv/bin/activate
echo "Current directory: \$(pwd)"
echo "Python path: \$(which python)"
ls -la manage.py
python manage.py migrate
python manage.py collectstatic --noinput
"@

ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP $djangoCommands

# 5. Restart services
Write-Host "Restarting services..." -ForegroundColor Blue
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo systemctl restart planit 2>/dev/null; echo 'planit service restart attempted'"
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "sudo systemctl restart nginx 2>/dev/null; echo 'nginx restart attempted'"

# 6. Check server status
Write-Host "Checking server status..." -ForegroundColor Blue
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "ps aux | grep python | grep -v grep"

Write-Host "Update completed!" -ForegroundColor Green
Write-Host "Check website: http://planit.boramae.club" -ForegroundColor Cyan
