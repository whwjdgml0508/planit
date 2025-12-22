$keyPath = "C:\Users\User\.ssh\ec2-kafa-2-key.pem"
$server = "ubuntu@35.163.12.109"

Write-Host "Checking production home.html file..." -ForegroundColor Cyan
ssh -i $keyPath $server "cat /home/ubuntu/planit/templates/home.html"
