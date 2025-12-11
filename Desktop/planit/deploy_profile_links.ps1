# PlanIt 프로필 통계 카드 링크 기능 배포 스크립트

Write-Host "=== PlanIt 프로필 통계 카드 링크 기능 배포 ===" -ForegroundColor Cyan
Write-Host ""

# 서버 정보
$SERVER = "ubuntu@35.163.12.109"
$KEY_PATH = "~/.ssh/ec2-kafa-2-key.pem"
$REMOTE_PATH = "/home/ubuntu/planit"

Write-Host "1. 변경된 파일을 서버로 복사 중..." -ForegroundColor Yellow

# templates/accounts/profile.html 복사
Write-Host "  - profile.html 복사 중..."
scp -i $KEY_PATH "templates/accounts/profile.html" "${SERVER}:${REMOTE_PATH}/templates/accounts/"

# community/views.py 복사
Write-Host "  - community/views.py 복사 중..."
scp -i $KEY_PATH "community/views.py" "${SERVER}:${REMOTE_PATH}/community/"

# templates/community/post_list.html 복사
Write-Host "  - post_list.html 복사 중..."
scp -i $KEY_PATH "templates/community/post_list.html" "${SERVER}:${REMOTE_PATH}/templates/community/"

Write-Host ""
Write-Host "2. 서버에서 서비스 재시작 중..." -ForegroundColor Yellow

ssh -i $KEY_PATH $SERVER @"
    cd $REMOTE_PATH
    
    # 파일 권한 설정
    sudo chown -R ubuntu:ubuntu templates/ community/
    
    # PlanIt 서비스 재시작
    sudo systemctl restart planit
    
    # 서비스 상태 확인
    echo ""
    echo "=== PlanIt 서비스 상태 ==="
    sudo systemctl status planit --no-pager -l
    
    echo ""
    echo "=== 최근 로그 확인 ==="
    sudo journalctl -u planit -n 20 --no-pager
"@

Write-Host ""
Write-Host "=== 배포 완료 ===" -ForegroundColor Green
Write-Host ""
Write-Host "변경 사항:" -ForegroundColor Cyan
Write-Host "  ✓ 프로필 통계 카드에 클릭 가능한 링크 추가"
Write-Host "    - 등록된 과목 → 시간표 관리 페이지"
Write-Host "    - 완료한 과제 → 과제 목록 페이지"
Write-Host "    - 커뮤니티 게시글 → 본인 게시글 목록"
Write-Host "  ✓ 통계 카드 호버 효과 추가"
Write-Host "  ✓ 커뮤니티 게시글 목록에 작성자 필터링 기능 추가"
Write-Host "  ✓ 필터링된 작성자 정보 표시"
Write-Host ""
Write-Host "테스트 URL: http://planit.boramae.club/accounts/profile/" -ForegroundColor Yellow
Write-Host ""
