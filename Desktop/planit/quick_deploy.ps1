# 빠른 배포 스크립트 - Git을 통한 코드 업데이트
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "서버에 접속하여 Git을 통해 최신 코드를 가져옵니다..." -ForegroundColor Blue

try {
    $deployCommand = @"
cd /home/ubuntu/planit
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
sudo systemctl restart planit
sudo systemctl restart nginx
"@
    
    ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP $deployCommand
    
    Write-Host "`n✅ 배포가 완료되었습니다!" -ForegroundColor Green
    Write-Host "🌐 사이트 확인: http://planit.boramae.club/" -ForegroundColor Cyan
    
} catch {
    Write-Host "❌ 오류 발생: $($_.Exception.Message)" -ForegroundColor Red
}
