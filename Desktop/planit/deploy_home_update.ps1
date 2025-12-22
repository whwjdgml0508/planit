# Deploy updated home.html to production server
$keyPath = "C:\Users\User\.ssh\ec2-kafa-2-key.pem"
$server = "ubuntu@35.163.12.109"

Write-Host "=== Deploying Home Page Update ===" -ForegroundColor Cyan

# Upload the updated home.html
Write-Host "`nUploading home.html..." -ForegroundColor Yellow
scp -i $keyPath "C:\Users\User\Desktop\planit\templates\home.html" "${server}:/tmp/home.html"

# Backup and replace
Write-Host "`nBacking up and replacing file..." -ForegroundColor Yellow
ssh -i $keyPath $server @"
sudo cp /home/ubuntu/planit/templates/home.html /home/ubuntu/planit/templates/home.html.backup
sudo mv /tmp/home.html /home/ubuntu/planit/templates/home.html
sudo chown ubuntu:ubuntu /home/ubuntu/planit/templates/home.html
"@

# Restart services
Write-Host "`nRestarting services..." -ForegroundColor Yellow
ssh -i $keyPath $server "sudo systemctl restart planit && sudo systemctl restart nginx"

Write-Host "`nWaiting for services..." -ForegroundColor Cyan
Start-Sleep -Seconds 5

# Check status
Write-Host "`nService status:" -ForegroundColor Yellow
ssh -i $keyPath $server "sudo systemctl is-active planit && sudo systemctl is-active nginx"

Write-Host "`n=== Deployment Complete! ===" -ForegroundColor Green
Write-Host "Check: http://planit.boramae.club/" -ForegroundColor Green
