# PlanIt 배포 가이드

## 개요
이 문서는 PlanIt Django 애플리케이션을 AWS EC2에 배포하는 방법을 설명합니다.

## 배포 환경
- **서버**: AWS EC2 (Ubuntu 22.04 LTS 권장)
- **웹서버**: Nginx
- **WSGI**: Gunicorn
- **데이터베이스**: PostgreSQL
- **캐시**: Redis
- **도메인**: http://planit.boramae.club

## 사전 준비사항

### 1. AWS EC2 인스턴스 설정
- Ubuntu 22.04 LTS 인스턴스 생성
- 보안 그룹에서 포트 80, 443, 22 열기
- 탄력적 IP 할당
- 도메인 DNS 설정 (planit.boramae.club → EC2 IP)

### 2. 로컬에서 필요한 작업
```bash
# 배포 스크립트에 실행 권한 부여
chmod +x deploy/deploy.sh
```

## 자동 배포 (권장)

### 1. EC2 인스턴스에 접속
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

### 2. 배포 스크립트 다운로드 및 실행
```bash
# 프로젝트 클론
git clone https://github.com/whwjdgml0508/cadet-learning-platform.git
cd cadet-learning-platform

# 배포 스크립트 실행
./deploy/deploy.sh
```

### 3. 환경변수 설정
```bash
# .env 파일 편집
nano .env

# 다음 값들을 실제 값으로 변경:
SECRET_KEY=your-very-secure-secret-key
DB_PASSWORD=your-secure-database-password
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-app-password
```

### 4. 서비스 재시작
```bash
sudo systemctl restart planit
sudo systemctl restart nginx
```

## 수동 배포

### 1. 시스템 패키지 업데이트
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. 필요한 패키지 설치
```bash
sudo apt install -y python3 python3-pip python3-venv python3-dev \
    postgresql postgresql-contrib nginx redis-server git curl \
    supervisor certbot python3-certbot-nginx
```

### 3. PostgreSQL 설정
```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE planit_db;
CREATE USER planit_user WITH PASSWORD 'your_secure_password';
ALTER ROLE planit_user SET client_encoding TO 'utf8';
ALTER ROLE planit_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE planit_user SET timezone TO 'Asia/Seoul';
GRANT ALL PRIVILEGES ON DATABASE planit_db TO planit_user;
\q
```

### 4. 프로젝트 설정
```bash
# 프로젝트 디렉토리 생성
sudo mkdir -p /var/www/planit
sudo chown -R $USER:www-data /var/www/planit

# 프로젝트 클론
git clone https://github.com/whwjdgml0508/cadet-learning-platform.git /var/www/planit
cd /var/www/planit

# 가상환경 생성
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. 환경변수 설정
```bash
cp .env.example .env
nano .env
```

### 6. Django 설정
```bash
export DJANGO_SETTINGS_MODULE=planit_project.settings.production
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py createsuperuser
```

### 7. Gunicorn 서비스 설정
```bash
sudo cp deploy/planit.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable planit
sudo systemctl start planit
```

### 8. Nginx 설정
```bash
sudo cp deploy/nginx_planit.conf /etc/nginx/sites-available/planit
sudo ln -s /etc/nginx/sites-available/planit /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 9. SSL 인증서 설정 (선택사항)
```bash
sudo certbot --nginx -d planit.boramae.club
```

## 배포 후 확인사항

### 1. 서비스 상태 확인
```bash
sudo systemctl status planit
sudo systemctl status nginx
sudo systemctl status postgresql
sudo systemctl status redis-server
```

### 2. 로그 확인
```bash
# Django 애플리케이션 로그
sudo journalctl -u planit -f

# Nginx 로그
sudo tail -f /var/log/nginx/planit_error.log
sudo tail -f /var/log/nginx/planit_access.log

# Gunicorn 로그
sudo tail -f /var/log/planit/gunicorn_error.log
```

### 3. 웹사이트 접속 테스트
- http://planit.boramae.club 접속 확인
- 관리자 페이지 접속: http://planit.boramae.club/admin/
- 정적 파일 로딩 확인

## 유지보수

### 1. 코드 업데이트
```bash
cd /var/www/planit
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart planit
```

### 2. 데이터베이스 백업
```bash
# 백업 생성
sudo -u postgres pg_dump planit_db > backup_$(date +%Y%m%d_%H%M%S).sql

# 백업 복원
sudo -u postgres psql planit_db < backup_file.sql
```

### 3. 로그 로테이션
로그 로테이션은 자동으로 설정되어 있습니다 (`/etc/logrotate.d/planit`).

## 보안 설정

### 1. 방화벽 설정
```bash
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
```

### 2. 정기 업데이트 설정
```bash
# 자동 보안 업데이트 활성화
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### 3. 모니터링 설정
```bash
# 시스템 모니터링을 위한 htop 설치
sudo apt install htop

# 디스크 사용량 모니터링
df -h
du -sh /var/www/planit/
```

## 문제 해결

### 1. 서비스가 시작되지 않는 경우
```bash
# 서비스 상태 확인
sudo systemctl status planit

# 로그 확인
sudo journalctl -u planit --no-pager

# 설정 파일 확인
python manage.py check --deploy
```

### 2. 정적 파일이 로드되지 않는 경우
```bash
# 정적 파일 재수집
python manage.py collectstatic --noinput

# 권한 확인
sudo chown -R www-data:www-data /var/www/planit/staticfiles/
```

### 3. 데이터베이스 연결 오류
```bash
# PostgreSQL 서비스 확인
sudo systemctl status postgresql

# 데이터베이스 연결 테스트
sudo -u postgres psql -c "SELECT version();"
```

## 성능 최적화

### 1. Redis 캐시 설정 확인
```bash
redis-cli ping
```

### 2. Gunicorn 워커 수 조정
`gunicorn.conf.py`에서 워커 수를 서버 사양에 맞게 조정하세요.

### 3. Nginx 캐시 설정
정적 파일에 대한 캐시 헤더가 설정되어 있습니다.

## 연락처
배포 관련 문제가 있을 경우 개발팀에 문의하세요.

---
**주의**: 프로덕션 환경에서는 반드시 강력한 비밀번호를 사용하고, 정기적으로 보안 업데이트를 적용하세요.
