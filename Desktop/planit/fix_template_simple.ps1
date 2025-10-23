# 템플릿 static 태그 오류 간단 수정
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "템플릿 오류 수정 중..." -ForegroundColor Yellow

# 1단계: 파일 확인
Write-Host "1. 현재 base.html 파일 확인..." -ForegroundColor Cyan
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /home/ubuntu/planit && head -n 3 templates/base.html"

# 2단계: 백업 및 수정
Write-Host "`n2. 파일 백업 및 수정..." -ForegroundColor Cyan
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /home/ubuntu/planit && cp templates/base.html templates/base.html.backup"

# 3단계: static 태그 추가
Write-Host "`n3. static 태그 추가..." -ForegroundColor Cyan
$addStaticCommand = @"
cd /home/ubuntu/planit
if ! head -n 1 templates/base.html | grep -q 'load static'; then
    echo '{% load static %}' > templates/base.html.tmp
    cat templates/base.html >> templates/base.html.tmp
    mv templates/base.html.tmp templates/base.html
    echo 'static 태그가 추가되었습니다.'
else
    echo 'static 태그가 이미 존재합니다.'
fi
"@

ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP $addStaticCommand

# 4단계: 수정 결과 확인
Write-Host "`n4. 수정 결과 확인..." -ForegroundColor Cyan
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /home/ubuntu/planit && head -n 3 templates/base.html"

# 5단계: 서버 재시작
Write-Host "`n5. 서버 재시작..." -ForegroundColor Cyan
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /home/ubuntu/planit && pkill -f python; source venv/bin/activate && nohup python manage.py runserver 0.0.0.0:8000 > server.log 2>&1 &"

Write-Host "`n✅ 수정 완료! 잠시 후 http://planit.boramae.club/ 를 확인해보세요." -ForegroundColor Green
