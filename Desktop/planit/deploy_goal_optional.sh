#!/bin/bash

echo "========================================"
echo "PlanIt 목표 설정 필드 선택사항 변경 배포"
echo "========================================"
echo ""

# SSH 연결 정보
SSH_KEY="~/.ssh/ec2-kafa-2-key.pem"
SSH_USER="ubuntu"
SSH_HOST="35.163.12.109"
PROJECT_PATH="/home/ubuntu/planit"

echo "[1/3] 서버에 연결하여 코드 업데이트..."
ssh -i $SSH_KEY "$SSH_USER@$SSH_HOST" << 'EOF'
    cd /home/ubuntu/planit
    git pull origin main
    echo '코드 업데이트 완료'
EOF

echo ""
echo "[2/3] Python 캐시 정리..."
ssh -i $SSH_KEY "$SSH_USER@$SSH_HOST" << 'EOF'
    cd /home/ubuntu/planit
    find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -delete 2>/dev/null || true
    echo 'Python 캐시 정리 완료'
EOF

echo ""
echo "[3/3] 서비스 재시작..."
ssh -i $SSH_KEY "$SSH_USER@$SSH_HOST" << 'EOF'
    sudo systemctl restart planit
    sudo systemctl restart nginx
    sleep 2
    sudo systemctl status planit --no-pager -l
EOF

echo ""
echo "========================================"
echo "배포 완료!"
echo "========================================"
echo ""
echo "변경 사항:"
echo "  - 목표 수치 설정 섹션 제목: '(최소 하나는 입력해주세요)' → '(선택사항)'"
echo "  - 목표 학습시간 라벨: '목표 학습시간 (시간)' → '목표 학습시간 (시간, 선택사항)'"
echo "  - 목표 과제 수 라벨: '목표 과제 수' → '목표 과제 수 (선택사항)'"
echo ""
echo "테스트 URL: http://planit.boramae.club/planner/goals/create/"
echo ""
