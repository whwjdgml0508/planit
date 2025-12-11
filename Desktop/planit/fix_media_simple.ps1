# PlanIt Media Files 404 오류 해결 스크립트

$sshKey = "~/.ssh/ec2-kafa-2-key.pem"
$server = "ubuntu@35.163.12.109"

Write-Host "=== PlanIt Media Files 404 오류 해결 ===" -ForegroundColor Cyan

Write-Host "`n1. 현재 상태 진단..." -ForegroundColor Yellow
ssh -i $sshKey $server "cd /home/ubuntu/planit && find media -type f 2>/dev/null | head -20"

Write-Host "`n2. /var/www/planit/media 디렉토리 생성..." -ForegroundColor Yellow
ssh -i $sshKey $server "sudo mkdir -p /var/www/planit/media/profiles /var/www/planit/media/posts /var/www/planit/media/comments"

Write-Host "`n3. 기존 media 파일 복사..." -ForegroundColor Yellow
ssh -i $sshKey $server "sudo cp -r /home/ubuntu/planit/media/* /var/www/planit/media/ 2>/dev/null || true"

Write-Host "`n4. 권한 설정..." -ForegroundColor Yellow
ssh -i $sshKey $server "sudo chown -R www-data:www-data /var/www/planit/media && sudo chmod -R 755 /var/www/planit/media"

Write-Host "`n5. 복사된 파일 확인..." -ForegroundColor Yellow
ssh -i $sshKey $server "ls -la /var/www/planit/media/profiles/"

Write-Host "`n6. production.py MEDIA_ROOT 수정..." -ForegroundColor Yellow
ssh -i $sshKey $server "cd /home/ubuntu/planit && sudo sed -i `"s|MEDIA_ROOT = os.path.join(BASE_DIR, 'media')|MEDIA_ROOT = '/var/www/planit/media'|g`" planit_project/settings/production.py"

Write-Host "`n7. 수정 확인..." -ForegroundColor Yellow
ssh -i $sshKey $server "cd /home/ubuntu/planit && grep -A 2 'Media files configuration' planit_project/settings/production.py"

Write-Host "`n8. 서비스 재시작..." -ForegroundColor Yellow
ssh -i $sshKey $server "sudo systemctl restart planit && sudo systemctl restart nginx"

Write-Host "`n9. 서비스 상태 확인..." -ForegroundColor Yellow
ssh -i $sshKey $server "sudo systemctl status planit --no-pager -l | head -15"

Write-Host "`n=== 완료! ===" -ForegroundColor Green
Write-Host "브라우저에서 프로필 이미지를 다시 클릭해보세요." -ForegroundColor White
