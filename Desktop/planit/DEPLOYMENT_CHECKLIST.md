# PlanIt EC2 배포 체크리스트

## 배포 전 준비사항

### 1. AWS EC2 설정
- [ ] Ubuntu 22.04 LTS EC2 인스턴스 생성
- [ ] 보안 그룹 설정 (포트 22, 80, 443 열기)
- [ ] 탄력적 IP 할당
- [ ] SSH 키 페어 생성 및 다운로드
- [ ] 도메인 DNS 설정 (planit.boramae.club → EC2 IP)

### 2. 로컬 환경 준비
- [ ] Git 저장소에 모든 변경사항 커밋 및 푸시
- [ ] `deploy.sh` 스크립트의 `REPO_URL` 변수를 실제 저장소 URL로 수정
- [ ] 배포 스크립트 실행 권한 확인 (`chmod +x deploy.sh`)

### 3. 환경 변수 준비
- [ ] Django SECRET_KEY 생성 준비
- [ ] 데이터베이스 비밀번호 준비
- [ ] 이메일 설정 정보 준비 (Gmail 앱 비밀번호 등)

## 배포 과정

### 1. EC2 인스턴스 접속
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```
- [ ] EC2 인스턴스에 성공적으로 접속

### 2. 자동 배포 실행
```bash
git clone https://github.com/whwjdgml0508/cadet-learning-platform.git
cd planit
chmod +x deploy.sh
./deploy.sh
```
- [ ] 프로젝트 클론 완료
- [ ] 배포 스크립트 실행 완료
- [ ] 시스템 패키지 업데이트 완료
- [ ] 필요한 패키지 설치 완료
- [ ] PostgreSQL 데이터베이스 설정 완료
- [ ] Python 가상환경 설정 완료
- [ ] Django 의존성 설치 완료
- [ ] 환경변수 설정 완료
- [ ] Django 마이그레이션 완료
- [ ] 정적 파일 수집 완료
- [ ] Django 슈퍼유저 생성 완료
- [ ] Gunicorn 서비스 설정 완료
- [ ] Nginx 설정 완료
- [ ] 방화벽 설정 완료
- [ ] Fail2ban 설정 완료
- [ ] 로그 로테이션 설정 완료

### 3. SSL 인증서 설정 (선택사항)
- [ ] Let's Encrypt SSL 인증서 설치
- [ ] HTTPS 리다이렉션 설정
- [ ] SSL 인증서 자동 갱신 설정

## 배포 후 검증

### 1. 서비스 상태 확인
```bash
sudo systemctl status planit
sudo systemctl status nginx
sudo systemctl status postgresql
```
- [ ] PlanIt 서비스 정상 실행
- [ ] Nginx 서비스 정상 실행
- [ ] PostgreSQL 서비스 정상 실행

### 2. 웹사이트 접속 테스트
- [ ] http://planit.boramae.club 접속 확인
- [ ] 메인 페이지 정상 로딩
- [ ] 정적 파일 (CSS, JS, 이미지) 정상 로딩
- [ ] 관리자 페이지 접속: http://planit.boramae.club/admin/
- [ ] 사용자 회원가입/로그인 테스트
- [ ] 각 앱 기능 테스트:
  - [ ] 계정 관리 (accounts)
  - [ ] 시간표 관리 (timetable)
  - [ ] 학습 플래너 (planner)
  - [ ] 커뮤니티 (community)

### 3. 로그 확인
```bash
# 애플리케이션 로그
sudo journalctl -u planit --no-pager -n 50

# Nginx 로그
sudo tail -n 50 /var/log/nginx/planit_error.log
sudo tail -n 50 /var/log/nginx/planit_access.log

# Gunicorn 로그
sudo tail -n 50 /var/log/planit/gunicorn_error.log
```
- [ ] 애플리케이션 로그에 오류 없음
- [ ] Nginx 로그에 심각한 오류 없음
- [ ] Gunicorn 로그에 오류 없음

### 4. 성능 및 보안 확인
- [ ] 페이지 로딩 속도 확인
- [ ] 방화벽 상태 확인 (`sudo ufw status`)
- [ ] Fail2ban 상태 확인 (`sudo fail2ban-client status`)
- [ ] SSL 인증서 상태 확인 (SSL 설정한 경우)

## 배포 후 설정

### 1. 환경변수 최종 확인
```bash
nano /var/www/planit/.env
```
- [ ] SECRET_KEY 설정 확인
- [ ] 데이터베이스 설정 확인
- [ ] 이메일 설정 확인
- [ ] ALLOWED_HOSTS 설정 확인

### 2. 추가 설정
- [ ] Django 관리자 계정으로 로그인하여 기본 데이터 입력
- [ ] 사이트 설정 확인 (Django Sites framework)
- [ ] 이메일 발송 테스트
- [ ] 파일 업로드 테스트

### 3. 모니터링 설정
- [ ] 시스템 리소스 모니터링 설정
- [ ] 로그 모니터링 설정
- [ ] 백업 스케줄 설정

## 문제 해결

### 일반적인 문제들
- [ ] 서비스가 시작되지 않는 경우: `sudo systemctl status planit` 확인
- [ ] 정적 파일이 로드되지 않는 경우: `python manage.py collectstatic --noinput` 재실행
- [ ] 데이터베이스 연결 오류: PostgreSQL 서비스 및 설정 확인
- [ ] 권한 오류: 파일 및 디렉토리 권한 확인 (`sudo chown -R www-data:www-data /var/www/planit`)

### 긴급 복구
- [ ] 백업에서 데이터베이스 복원 방법 숙지
- [ ] 이전 버전으로 롤백 방법 숙지
- [ ] 로그 파일 위치 및 확인 방법 숙지

## 유지보수 계획

### 정기 작업
- [ ] 주간 시스템 업데이트 스케줄
- [ ] 월간 데이터베이스 백업 확인
- [ ] 분기별 보안 점검
- [ ] SSL 인증서 만료일 확인 (3개월마다)

### 모니터링
- [ ] 서버 리소스 사용량 모니터링
- [ ] 애플리케이션 오류 로그 모니터링
- [ ] 웹사이트 가용성 모니터링

---

**배포 완료 확인**: 모든 체크리스트 항목이 완료되면 배포가 성공적으로 완료된 것입니다.

**배포 일시**: _______________
**배포자**: _______________
**버전**: _______________
