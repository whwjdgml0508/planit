# 🚀 자동 배포 설정 가이드

GitHub에 푸시하면 자동으로 서버에 배포되도록 설정하는 방법입니다.

## 방법 1: GitHub Actions (추천)

### 1. GitHub Secrets 설정
GitHub 저장소 → Settings → Secrets and variables → Actions에서 다음 설정:

- `HOST`: 서버 IP 주소 (예: planit.boramae.club)
- `USERNAME`: 서버 사용자명 (예: ubuntu)
- `SSH_KEY`: 서버 접속용 SSH 개인키

### 2. 서버에서 SSH 키 설정
```bash
# 서버에서 실행
ssh-keygen -t rsa -b 4096 -C "github-actions"
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
cat ~/.ssh/id_rsa  # 이 내용을 GitHub Secrets의 SSH_KEY에 입력
```

### 3. 자동 배포 테스트
```bash
git add .
git commit -m "Test auto deployment"
git push origin main
```

## 방법 2: GitHub Webhook

### 1. 서버에서 웹훅 서버 실행
```bash
cd /home/ubuntu/planit
python3 deploy/webhook_server.py &
```

### 2. GitHub 웹훅 설정
GitHub 저장소 → Settings → Webhooks → Add webhook:
- URL: `http://your-server:9000/webhook`
- Content type: `application/json`
- Events: `Just the push event`

### 3. 방화벽 설정 (필요시)
```bash
sudo ufw allow 9000
```

## 방법 3: 간단한 수동 배포

서버에서 다음 스크립트 실행:
```bash
cd /home/ubuntu/planit
./deploy/auto_deploy.sh
```

## 🔧 문제 해결

### 권한 오류
```bash
chmod +x deploy/auto_deploy.sh
chmod +x deploy/webhook_server.py
```

### 서비스 재시작 권한
```bash
# sudoers 파일에 추가
sudo visudo
# 다음 줄 추가:
ubuntu ALL=(ALL) NOPASSWD: /bin/systemctl restart planit
```

## ✅ 배포 확인

배포 후 다음 URL에서 확인:
- 홈페이지: http://planit.boramae.club
- 설치 페이지: http://planit.boramae.club/install/

새로운 다운로드 버튼들이 보이면 성공! 🎉
