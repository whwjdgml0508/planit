# Remove "홈 화면에 추가" button from navigation bar
$keyPath = "C:\Users\User\.ssh\ec2-kafa-2-key.pem"
$server = "ubuntu@35.163.12.109"

Write-Host "Removing '홈 화면에 추가' button from navigation..." -ForegroundColor Yellow

# Create a backup and remove the button using sed
ssh -i $keyPath $server @'
cd /home/ubuntu/planit/templates
sudo cp base.html base.html.backup_$(date +%Y%m%d_%H%M%S)
sudo sed -i '/<!-- 홈 화면에 추가 링크/,/<\/li>/d' base.html
'@

Write-Host "`nRestarting services..." -ForegroundColor Yellow
ssh -i $keyPath $server "sudo systemctl restart planit && sudo systemctl restart nginx"

Start-Sleep -Seconds 5

Write-Host "`nVerifying changes..." -ForegroundColor Yellow
$result = ssh -i $keyPath $server "grep -c '홈 화면에 추가' /home/ubuntu/planit/templates/base.html || echo '0'"

if ($result -match "0") {
    Write-Host "✓ Button successfully removed!" -ForegroundColor Green
} else {
    Write-Host "✗ Button still present" -ForegroundColor Red
}

Write-Host "`nChecking service status..." -ForegroundColor Yellow
ssh -i $keyPath $server "sudo systemctl is-active planit && sudo systemctl is-active nginx"

Write-Host "`nDone! Check: http://planit.boramae.club/" -ForegroundColor Green
