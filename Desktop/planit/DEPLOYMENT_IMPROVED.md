# 🚀 PlanIt 개선된 배포 가이드

## 📋 개선 사항 요약

중간발표 채점 결과를 바탕으로 다음 사항들이 개선되었습니다:

### ✅ 해결된 문제들
- **README.md 화면 섹션 추가** - 스크린샷 섹션과 자동 촬영 도구 제공
- **HTTPS 설정** - Let's Encrypt SSL 인증서 자동 설정 스크립트
- **Docker 컨테이너화** - 완전한 Docker 및 Docker Compose 설정
- **설정 파일 추가** - Makefile, .dockerignore 등 프로젝트 구조 개선

### 📊 점수 개선 예상
- **배포 및 접근성**: +4.0점 (HTTPS 적용)
- **README 및 문서화**: +4.9점 (화면 섹션 및 스크린샷 추가)
- **코드 구조 및 품질**: +8.0점 (Docker, 설정 파일 추가)

---

## 🔒 1. HTTPS 설정 (우선순위: 높음)

### 자동 SSL 설정
```bash
# SSL 인증서 자동 발급 및 설정
chmod +x deploy/setup_ssl.sh
./deploy/setup_ssl.sh
```

### 수동 SSL 설정
```bash
# Certbot 설치
sudo apt update
sudo apt install -y certbot python3-certbot-nginx

# SSL 인증서 발급
sudo certbot --nginx -d planit.boramae.club --email admin@boramae.club --agree-tos --non-interactive

# 자동 갱신 설정
sudo crontab -e
# 다음 줄 추가: 0 12 * * * /usr/bin/certbot renew --quiet
```

### HTTPS 확인
```bash
# SSL 등급 확인
curl -I https://planit.boramae.club

# SSL Labs 테스트
# https://www.ssllabs.com/ssltest/analyze.html?d=planit.boramae.club
```

---

## 📸 2. 스크린샷 추가 (우선순위: 높음)

### 자동 스크린샷 촬영
```bash
# Playwright 설치 및 스크린샷 촬영
pip install playwright
python -m playwright install chromium
python take_screenshots.py
```

### 수동 스크린샷 촬영
1. **브라우저에서 F12 → Ctrl+Shift+P → "screenshot"**
2. **필요한 페이지들**:
   - 메인 페이지: http://planit.boramae.club/
   - 시간표: http://planit.boramae.club/timetable/
   - 플래너: http://planit.boramae.club/planner/
   - 커뮤니티: http://planit.boramae.club/community/
   - 관리자: http://planit.boramae.club/admin/

### 스크린샷 파일 위치
```
screenshots/
├── main_page.png
├── timetable.png
├── planner.png
├── community.png
├── mobile_app.png
└── admin_page.png
```

---

## 🐳 3. Docker 컨테이너화 (우선순위: 중간)

### 개발 환경 Docker 실행
```bash
# Docker 이미지 빌드
docker-compose build

# 컨테이너 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f
```

### 프로덕션 환경 Docker 실행
```bash
# 환경 변수 설정
cp .env.example .env
# .env 파일 편집 필요

# 프로덕션 컨테이너 시작
docker-compose -f docker-compose.prod.yml up -d

# SSL 인증서 초기 발급
chmod +x deploy/init_ssl.sh
./deploy/init_ssl.sh
```

### Docker 관리 명령어
```bash
# 컨테이너 상태 확인
docker-compose ps

# 컨테이너 중지
docker-compose down

# 볼륨 포함 완전 삭제
docker-compose down -v
```

---

## ⚙️ 4. 설정 파일 개선

### Makefile 사용법
```bash
# 도움말 보기
make help

# 개발 서버 실행
make dev

# Docker 빌드 및 실행
make docker-build
make docker-up

# 스크린샷 촬영
make screenshots

# SSL 설정
make ssl
```

### 환경 변수 설정
```bash
# .env 파일 생성
cp .env.example .env

# 필수 설정 항목들
SECRET_KEY=your-secret-key-here
DB_PASSWORD=your-secure-password
REDIS_PASSWORD=your-redis-password
ALLOWED_HOSTS=planit.boramae.club,www.planit.boramae.club
```

---

## 🔧 5. 추가 개선 사항

### 성능 최적화
```bash
# 정적 파일 압축 설정 (nginx.conf에 이미 포함됨)
# Gzip 압축, 캐싱 헤더 설정 완료

# 데이터베이스 최적화
python manage.py dbshell
# 인덱스 추가, 쿼리 최적화 등
```

### 보안 강화
```bash
# 방화벽 설정
sudo ufw enable
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS

# 자동 보안 업데이트
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### 모니터링 설정
```bash
# 로그 모니터링
tail -f /var/log/nginx/planit_access.log
tail -f /var/log/nginx/planit_error.log

# 시스템 리소스 모니터링
htop
df -h
free -h
```

---

## 📈 6. 배포 체크리스트

### 배포 전 확인사항
- [ ] `.env` 파일 설정 완료
- [ ] 데이터베이스 백업 완료
- [ ] 정적 파일 수집 완료
- [ ] SSL 인증서 발급 완료
- [ ] 방화벽 설정 완료

### 배포 후 확인사항
- [ ] HTTPS 접속 확인 (https://planit.boramae.club)
- [ ] 모든 페이지 정상 작동 확인
- [ ] 관리자 페이지 접속 확인
- [ ] 모바일 반응형 확인
- [ ] SSL 등급 A+ 확인

### 성능 테스트
```bash
# 응답 시간 테스트
curl -w "@curl-format.txt" -o /dev/null -s https://planit.boramae.club

# 동시 접속 테스트
ab -n 100 -c 10 https://planit.boramae.club/
```

---

## 🎯 7. 향후 개선 계획 (2-3주)

### 1주차 목표
- [x] HTTPS 적용 완료
- [x] README 스크린샷 섹션 추가
- [x] Docker 컨테이너화 완료

### 2주차 목표
- [ ] CI/CD 파이프라인 구축 (GitHub Actions)
- [ ] 자동화된 테스트 환경 구축
- [ ] 성능 모니터링 대시보드 구축

### 3주차 목표
- [ ] CDN 적용 (CloudFlare)
- [ ] 데이터베이스 최적화
- [ ] 보안 감사 및 개선

---

## 📞 문제 해결

### 일반적인 문제들
1. **HTTPS 인증서 발급 실패**
   - DNS 설정 확인
   - 도메인 소유권 확인
   - 방화벽 80/443 포트 열기

2. **Docker 컨테이너 시작 실패**
   - 포트 충돌 확인
   - 환경 변수 설정 확인
   - 로그 확인: `docker-compose logs`

3. **정적 파일 로드 실패**
   - `python manage.py collectstatic` 실행
   - nginx 설정 확인
   - 파일 권한 확인

### 로그 위치
- **Nginx**: `/var/log/nginx/planit_*.log`
- **Django**: `server.log`
- **Docker**: `docker-compose logs`

---

## 🎉 완료!

이제 PlanIt 프로젝트가 다음과 같이 개선되었습니다:

- ✅ **HTTPS 보안 연결** - Let's Encrypt SSL 인증서
- ✅ **완전한 README** - 스크린샷 섹션 포함
- ✅ **Docker 컨테이너화** - 개발/프로덕션 환경 분리
- ✅ **자동화 도구** - Makefile, 스크린샷 도구 등
- ✅ **보안 강화** - 방화벽, 보안 헤더 설정

**예상 점수 개선: +16.9점** 🎯
