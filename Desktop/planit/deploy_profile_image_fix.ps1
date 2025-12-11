# PlanIt 프로필 이미지 업로드 수정 배포 스크립트
# 프로필 이미지가 업로드되고 표시되도록 수정

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "PlanIt 프로필 이미지 수정 배포 시작" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# 서버 정보
$SERVER = "ubuntu@35.163.12.109"
$KEY_PATH = "$env:USERPROFILE\.ssh\ec2-kafa-2-key.pem"
$REMOTE_DIR = "/home/ubuntu/planit"
$MEDIA_DIR = "/var/www/planit/media"

Write-Host "[1/6] 로컬 변경사항 Git 커밋..." -ForegroundColor Yellow
git add accounts/views.py accounts/models.py templates/base.html templates/community/*.html
git commit -m "Fix: 프로필 이미지 업로드 및 표시 기능 완전 수정

- ProfileEditView에서 파일 업로드 명시적 처리 추가
- 기존 이미지 자동 삭제 로직 추가
- User 모델에 get_avatar_emoji() 메서드 추가
- 모든 템플릿에서 get_avatar_emoji 사용하도록 수정
- 로깅 추가로 디버깅 개선"

Write-Host "[2/6] GitHub에 푸시..." -ForegroundColor Yellow
git push origin main

Write-Host "[3/6] 서버에 연결하여 코드 업데이트..." -ForegroundColor Yellow
ssh -i $KEY_PATH $SERVER @"
    cd $REMOTE_DIR && \
    git pull origin main && \
    echo '코드 업데이트 완료'
"@

Write-Host "[4/6] media 디렉토리 권한 확인 및 생성..." -ForegroundColor Yellow
ssh -i $KEY_PATH $SERVER @"
    # media 디렉토리 생성 (없으면)
    sudo mkdir -p $MEDIA_DIR && \
    sudo mkdir -p $MEDIA_DIR/profiles && \
    
    # 소유권 변경
    sudo chown -R ubuntu:www-data $MEDIA_DIR && \
    
    # 권한 설정 (775)
    sudo chmod -R 775 $MEDIA_DIR && \
    
    # 확인
    ls -la $MEDIA_DIR && \
    echo 'media 디렉토리 권한 설정 완료'
"@

Write-Host "[5/6] Django 서비스 재시작..." -ForegroundColor Yellow
ssh -i $KEY_PATH $SERVER @"
    sudo systemctl restart planit && \
    sleep 3 && \
    sudo systemctl status planit --no-pager
"@

Write-Host "[6/6] 배포 완료 확인..." -ForegroundColor Yellow
ssh -i $KEY_PATH $SERVER @"
    echo '=== PlanIt 서비스 상태 ===' && \
    sudo systemctl is-active planit && \
    echo '' && \
    echo '=== Media 디렉토리 구조 ===' && \
    ls -lah $MEDIA_DIR && \
    echo '' && \
    echo '=== 최근 로그 (마지막 20줄) ===' && \
    sudo journalctl -u planit -n 20 --no-pager
"@

Write-Host ""
Write-Host "=====================================" -ForegroundColor Green
Write-Host "배포 완료!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""
Write-Host "테스트 방법:" -ForegroundColor Cyan
Write-Host "1. http://planit.boramae.club/accounts/profile/ 접속" -ForegroundColor White
Write-Host "2. '프로필 수정' 버튼 클릭" -ForegroundColor White
Write-Host "3. 프로필 이미지 업로드" -ForegroundColor White
Write-Host "4. 저장 후 프로필 페이지에서 이미지 확인" -ForegroundColor White
Write-Host "5. 네비게이션 바, 커뮤니티 등 모든 위치에서 이미지 표시 확인" -ForegroundColor White
Write-Host ""
Write-Host "주요 수정사항:" -ForegroundColor Cyan
Write-Host "- ProfileEditView에서 파일 업로드 명시적 처리" -ForegroundColor White
Write-Host "- 기존 이미지 자동 삭제 및 교체" -ForegroundColor White
Write-Host "- media 디렉토리 권한 설정 (775)" -ForegroundColor White
Write-Host "- 로깅 추가로 문제 추적 가능" -ForegroundColor White
Write-Host ""
