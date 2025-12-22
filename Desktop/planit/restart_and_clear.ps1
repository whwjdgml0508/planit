# Restart services and clear cache
$keyPath = "C:\Users\User\.ssh\ec2-kafa-2-key.pem"
$server = "ubuntu@35.163.12.109"

Write-Host "Restarting services with full cache clear..." -ForegroundColor Yellow

ssh -i $keyPath $server @"
sudo systemctl stop planit
sudo rm -rf /home/ubuntu/planit/__pycache__
sudo rm -rf /home/ubuntu/planit/*/__pycache__
sudo rm -rf /home/ubuntu/planit/*/*/__pycache__
sudo systemctl start planit
sudo systemctl restart nginx
"@

Start-Sleep -Seconds 5

Write-Host "`nChecking status..." -ForegroundColor Yellow
ssh -i $keyPath $server "sudo systemctl is-active planit && sudo systemctl is-active nginx"

Write-Host "`nDone!" -ForegroundColor Green
