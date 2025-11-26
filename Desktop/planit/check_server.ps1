# 서버 상태 확인 스크립트
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "서버 상태를 확인합니다..." -ForegroundColor Blue

try {
    $checkCommand = @"
echo "=== 현재 디렉토리 ==="
pwd
echo "=== 홈 디렉토리 내용 ==="
ls -la ~/
echo "=== planit 디렉토리 확인 ==="
ls -la ~/planit/ 2>/dev/null || echo "planit 디렉토리가 없습니다"
echo "=== /var/www 확인 ==="
sudo ls -la /var/www/ 2>/dev/null || echo "/var/www/planit 디렉토리가 없습니다"
echo "=== 서비스 상태 ==="
sudo systemctl status planit --no-pager || echo "planit 서비스가 없습니다"
echo "=== nginx 상태 ==="
sudo systemctl status nginx --no-pager
"@
    
    ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP $checkCommand
    
} catch {
    Write-Host "❌ 오류 발생: $($_.Exception.Message)" -ForegroundColor Red
}
