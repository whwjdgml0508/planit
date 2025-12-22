# Quick fix for home.html template error
$keyPath = "C:\Users\User\.ssh\ec2-kafa-2-key.pem"
$server = "ubuntu@35.163.12.109"

Write-Host "Uploading corrected home.html..." -ForegroundColor Yellow
scp -i $keyPath "C:\Users\User\Desktop\planit\templates\home.html" "${server}:/tmp/home.html"

Write-Host "Replacing file..." -ForegroundColor Yellow
ssh -i $keyPath $server "sudo mv /tmp/home.html /home/ubuntu/planit/templates/home.html && sudo chown ubuntu:ubuntu /home/ubuntu/planit/templates/home.html"

Write-Host "Restarting services..." -ForegroundColor Yellow
ssh -i $keyPath $server "sudo systemctl restart planit"

Start-Sleep -Seconds 3

Write-Host "Done!" -ForegroundColor Green
