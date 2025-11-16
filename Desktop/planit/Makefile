# PlanIt 프로젝트 Makefile
# 자주 사용하는 명령어들을 간편하게 실행할 수 있습니다.

.PHONY: help install dev test clean build deploy docker-build docker-up docker-down screenshots ssl

# 기본 도움말
help:
	@echo "🚀 PlanIt 프로젝트 명령어"
	@echo ""
	@echo "개발 환경:"
	@echo "  install     - 의존성 패키지 설치"
	@echo "  dev         - 개발 서버 실행"
	@echo "  test        - 테스트 실행"
	@echo "  clean       - 캐시 및 임시 파일 정리"
	@echo ""
	@echo "배포:"
	@echo "  build       - 프로덕션 빌드"
	@echo "  deploy      - EC2 배포"
	@echo ""
	@echo "Docker:"
	@echo "  docker-build - Docker 이미지 빌드"
	@echo "  docker-up   - Docker 컨테이너 시작"
	@echo "  docker-down - Docker 컨테이너 중지"
	@echo ""
	@echo "유틸리티:"
	@echo "  screenshots - 자동 스크린샷 촬영"
	@echo "  ssl         - SSL 인증서 설정"

# 개발 환경 설정
install:
	@echo "📦 의존성 패키지 설치 중..."
	pip install -r requirements.txt
	python manage.py migrate
	@echo "✅ 설치 완료!"

# 개발 서버 실행
dev:
	@echo "🚀 개발 서버 시작 중..."
	python manage.py runserver

# 테스트 실행
test:
	@echo "🧪 테스트 실행 중..."
	python manage.py test

# 정리
clean:
	@echo "🧹 정리 중..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	@echo "✅ 정리 완료!"

# 프로덕션 빌드
build:
	@echo "🏗️ 프로덕션 빌드 중..."
	python manage.py collectstatic --noinput
	@echo "✅ 빌드 완료!"

# EC2 배포
deploy:
	@echo "🚀 EC2 배포 중..."
	chmod +x deploy/simple-deploy.sh
	./deploy/simple-deploy.sh

# Docker 이미지 빌드
docker-build:
	@echo "🐳 Docker 이미지 빌드 중..."
	docker-compose build

# Docker 컨테이너 시작 (개발용)
docker-up:
	@echo "🐳 Docker 컨테이너 시작 중..."
	docker-compose up -d

# Docker 컨테이너 시작 (프로덕션용)
docker-up-prod:
	@echo "🐳 프로덕션 Docker 컨테이너 시작 중..."
	docker-compose -f docker-compose.prod.yml up -d

# Docker 컨테이너 중지
docker-down:
	@echo "🐳 Docker 컨테이너 중지 중..."
	docker-compose down

# 프로덕션 Docker 컨테이너 중지
docker-down-prod:
	@echo "🐳 프로덕션 Docker 컨테이너 중지 중..."
	docker-compose -f docker-compose.prod.yml down

# 자동 스크린샷 촬영
screenshots:
	@echo "📸 스크린샷 촬영 중..."
	python take_screenshots.py

# SSL 인증서 설정
ssl:
	@echo "🔒 SSL 인증서 설정 중..."
	chmod +x deploy/setup_ssl.sh
	./deploy/setup_ssl.sh

# 로그 확인
logs:
	@echo "📋 로그 확인 중..."
	docker-compose logs -f

# 프로덕션 로그 확인
logs-prod:
	@echo "📋 프로덕션 로그 확인 중..."
	docker-compose -f docker-compose.prod.yml logs -f

# 데이터베이스 백업
backup:
	@echo "💾 데이터베이스 백업 중..."
	python manage.py dumpdata > backup_$(shell date +%Y%m%d_%H%M%S).json

# 마이그레이션
migrate:
	@echo "🔄 마이그레이션 실행 중..."
	python manage.py makemigrations
	python manage.py migrate

# 슈퍼유저 생성
superuser:
	@echo "👤 슈퍼유저 생성 중..."
	python manage.py createsuperuser

# 정적 파일 수집
collectstatic:
	@echo "📁 정적 파일 수집 중..."
	python manage.py collectstatic --noinput
