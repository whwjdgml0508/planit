Write-Host "🔧 템플릿 static 태그 오류 수정 중..." -ForegroundColor Yellow

# SSH를 통해 서버에 연결하여 수정 실행
$sshCommand = @"
cd /home/ubuntu/planit &&
source /home/ubuntu/planit/planit/venv/bin/activate &&
echo "📝 base.html 파일 확인 중..." &&
FIRST_LINE=`$(head -n 1 templates/base.html) &&
if [[ "`$FIRST_LINE" != "{% load static %}" ]]; then
    echo "❌ base.html 파일에 {% load static %} 태그가 없습니다. 수정 중..." &&
    cp templates/base.html templates/base.html.backup &&
    echo "{% load static %}" > templates/base.html.tmp &&
    cat templates/base.html >> templates/base.html.tmp &&
    mv templates/base.html.tmp templates/base.html &&
    echo "✅ base.html 파일이 수정되었습니다."
else
    echo "✅ base.html 파일이 이미 올바릅니다."
fi &&
echo "📁 정적 파일 재수집 중..." &&
python manage.py collectstatic --noinput &&
echo "🔄 서버 재시작 중..." &&
pkill -f python &&
pkill -f gunicorn &&
nohup python manage.py runserver 127.0.0.1:8000 > server.log 2>&1 & &&
echo "✅ 템플릿 static 태그 오류 수정 완료!" &&
echo "🌐 사이트를 다시 확인해보세요: http://planit.boramae.club/"
"@

try {
    Write-Host "🔗 SSH를 통해 서버에 연결 중..." -ForegroundColor Cyan
    
    # SSH 연결 (사용자가 SSH 키를 설정했다고 가정)
    ssh ubuntu@planit.boramae.club $sshCommand
    
    Write-Host "✅ 수정 작업이 완료되었습니다!" -ForegroundColor Green
    Write-Host "🌐 브라우저에서 http://planit.boramae.club/ 를 확인해보세요." -ForegroundColor Cyan
}
catch {
    Write-Host "❌ SSH 연결 실패: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "💡 수동으로 서버에 접속하여 다음 명령을 실행하세요:" -ForegroundColor Yellow
    Write-Host $sshCommand -ForegroundColor White
}
