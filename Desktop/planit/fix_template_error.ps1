# 템플릿 static 태그 오류 수정 스크립트
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "🔧 템플릿 static 태그 오류 수정 중..." -ForegroundColor Yellow

try {
    $fixCommand = @"
cd /home/ubuntu/planit &&
echo "📝 현재 base.html 파일 첫 번째 줄 확인..." &&
head -n 1 templates/base.html &&
echo "🔍 {% load static %} 태그 존재 여부 확인 중..." &&
if ! grep -q "{% load static %}" templates/base.html; then
    echo "❌ {% load static %} 태그가 없습니다. 수정 중..." &&
    cp templates/base.html templates/base.html.backup &&
    echo "{% load static %}" > templates/base.html.tmp &&
    cat templates/base.html >> templates/base.html.tmp &&
    mv templates/base.html.tmp templates/base.html &&
    echo "✅ base.html 파일에 {% load static %} 태그를 추가했습니다."
else
    echo "✅ {% load static %} 태그가 이미 존재합니다."
fi &&
echo "📝 수정 후 첫 번째 줄 확인..." &&
head -n 1 templates/base.html &&
echo "🔄 서버 재시작 중..." &&
pkill -f python &&
pkill -f gunicorn &&
source venv/bin/activate &&
nohup python manage.py runserver 0.0.0.0:8000 > server.log 2>&1 & &&
echo "✅ 서버가 재시작되었습니다." &&
echo "🌐 사이트 확인: http://planit.boramae.club/"
"@
    
    Write-Host "🔗 SSH를 통해 서버에 연결하여 수정 중..." -ForegroundColor Cyan
    
    ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP $fixCommand
    
    Write-Host "`n✅ 템플릿 오류 수정이 완료되었습니다!" -ForegroundColor Green
    Write-Host "🌐 브라우저에서 http://planit.boramae.club/ 를 다시 확인해보세요." -ForegroundColor Cyan
    
} catch {
    Write-Host "❌ 오류 발생: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "💡 수동으로 서버에 접속하여 확인이 필요할 수 있습니다." -ForegroundColor Yellow
}
