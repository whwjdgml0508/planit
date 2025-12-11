#!/bin/bash
# PlanIt Media Files 404 오류 해결 스크립트

echo "=== 1. 현재 상태 진단 ==="
echo "Django MEDIA_ROOT 위치:"
cd /home/ubuntu/planit
python3 manage.py shell << 'PYEOF'
from django.conf import settings
import os
print(f'MEDIA_ROOT: {settings.MEDIA_ROOT}')
print(f'MEDIA_URL: {settings.MEDIA_URL}')
print(f'MEDIA_ROOT exists: {os.path.exists(settings.MEDIA_ROOT)}')
PYEOF

echo ""
echo "업로드된 프로필 이미지 파일 찾기:"
find /home/ubuntu/planit/media -type f 2>/dev/null | head -20

echo ""
echo "=== 2. /var/www/planit/media 디렉토리 생성 및 복사 ==="
# media 디렉토리 구조 생성
sudo mkdir -p /var/www/planit/media/profiles
sudo mkdir -p /var/www/planit/media/posts
sudo mkdir -p /var/www/planit/media/comments

# 기존 media 파일 복사
if [ -d "/home/ubuntu/planit/media" ]; then
    echo "기존 media 파일 복사 중..."
    sudo cp -r /home/ubuntu/planit/media/* /var/www/planit/media/ 2>/dev/null || true
fi

# 권한 설정
sudo chown -R www-data:www-data /var/www/planit/media
sudo chmod -R 755 /var/www/planit/media

echo ""
echo "복사 후 파일 확인:"
ls -la /var/www/planit/media/
ls -la /var/www/planit/media/profiles/ 2>/dev/null

echo ""
echo "=== 3. production.py MEDIA_ROOT 수정 ==="
cd /home/ubuntu/planit
# MEDIA_ROOT을 /var/www/planit/media로 변경
sudo sed -i "s|MEDIA_ROOT = os.path.join(BASE_DIR, 'media')|MEDIA_ROOT = '/var/www/planit/media'|g" planit_project/settings/production.py

echo "수정된 설정 확인:"
grep -A 2 "Media files configuration" planit_project/settings/production.py

echo ""
echo "=== 4. nginx 설정 확인 ==="
echo "현재 nginx media 설정:"
grep -A 3 "location /media/" /etc/nginx/sites-enabled/planit

echo ""
echo "=== 5. 서비스 재시작 ==="
sudo systemctl restart planit
sudo systemctl restart nginx

echo ""
echo "=== 6. 서비스 상태 확인 ==="
sudo systemctl status planit --no-pager -l | head -20
sudo systemctl status nginx --no-pager -l | head -10

echo ""
echo "=== 7. 최종 확인 ==="
echo "업로드된 파일 목록:"
ls -la /var/www/planit/media/profiles/

echo ""
echo "완료! 브라우저에서 프로필 이미지 링크를 다시 클릭해보세요."
