# PlanIt 목표 설정 필드 선택사항 변경 배포 스크립트

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "PlanIt 목표 설정 필드 선택사항 변경 배포" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# SSH 연결 정보
$SSH_KEY = "~/.ssh/ec2-kafa-2-key.pem"
$SSH_USER = "ubuntu"
$SSH_HOST = "35.163.12.109"
$PROJECT_PATH = "/home/ubuntu/planit"

Write-Host "[1/4] Git 변경사항 커밋 및 푸시..." -ForegroundColor Yellow
git add planner/forms.py
git commit -m "목표 설정 필드를 완전히 선택사항으로 변경 - '최소 하나는 입력해주세요' 문구 제거"
git push origin main

Write-Host ""
Write-Host "[2/4] 서버에 연결하여 코드 업데이트..." -ForegroundColor Yellow
ssh -i $SSH_KEY "$SSH_USER@$SSH_HOST" @"
    cd $PROJECT_PATH
    git pull origin main
    echo '코드 업데이트 완료'
"@

Write-Host ""
Write-Host "[3/4] 수정된 파일 복사..." -ForegroundColor Yellow
ssh -i $SSH_KEY "$SSH_USER@$SSH_HOST" @"
    cd $PROJECT_PATH
    cp planner/forms.py planner/forms.py.bak
    echo 'forms.py 백업 완료'
"@

Write-Host ""
Write-Host "[4/4] 서비스 재시작..." -ForegroundColor Yellow
ssh -i $SSH_KEY "$SSH_USER@$SSH_HOST" @"
    sudo systemctl restart planit
    sudo systemctl restart nginx
    echo '서비스 재시작 완료'
"@

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "배포 완료!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "변경 사항:" -ForegroundColor Cyan
Write-Host "  - 목표 수치 설정 섹션 제목: '(최소 하나는 입력해주세요)' → '(선택사항)'" -ForegroundColor White
Write-Host "  - 목표 학습시간 라벨: '목표 학습시간 (시간)' → '목표 학습시간 (시간, 선택사항)'" -ForegroundColor White
Write-Host "  - 목표 과제 수 라벨: '목표 과제 수' → '목표 과제 수 (선택사항)'" -ForegroundColor White
Write-Host ""
Write-Host "테스트 URL: http://planit.boramae.club/planner/goals/create/" -ForegroundColor Cyan
Write-Host ""
