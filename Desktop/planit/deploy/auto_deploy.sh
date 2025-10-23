#!/bin/bash

# 자동 배포 스크립트
echo "🚀 자동 배포 시작..."

# 프로젝트 디렉토리로 이동
cd /home/ubuntu/planit

# 최신 코드 가져오기
echo "📥 최신 코드 가져오는 중..."
git pull origin main

# 가상환경 활성화
source venv/bin/activate

# 의존성 설치
echo "📦 의존성 업데이트 중..."
pip install -r requirements.txt

# 데이터베이스 마이그레이션
echo "🗄️ 데이터베이스 업데이트 중..."
python manage.py migrate

# 정적 파일 수집
echo "📁 정적 파일 수집 중..."
python manage.py collectstatic --noinput

# 서버 재시작
echo "🔄 서버 재시작 중..."
sudo systemctl restart planit

echo "✅ 자동 배포 완료!"
echo "🌐 사이트 확인: http://planit.boramae.club"
