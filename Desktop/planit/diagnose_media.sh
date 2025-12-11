#!/bin/bash
# PlanIt Media Files 404 오류 진단 스크립트

echo "=== Media 디렉토리 구조 확인 ==="
ls -la /home/ubuntu/planit/media/ 2>/dev/null || echo 'media 디렉토리 없음'
ls -la /var/www/planit/media/ 2>/dev/null || echo '/var/www/planit/media 디렉토리 없음'
echo ''

echo "=== profiles 디렉토리 확인 ==="
ls -la /home/ubuntu/planit/media/profiles/ 2>/dev/null || echo 'profiles 디렉토리 없음'
ls -la /var/www/planit/media/profiles/ 2>/dev/null || echo '/var/www/planit/media/profiles 디렉토리 없음'
echo ''

echo "=== Django MEDIA_ROOT 설정 확인 ==="
cd /home/ubuntu/planit
python3 manage.py shell << 'PYEOF'
from django.conf import settings
print(f'MEDIA_ROOT: {settings.MEDIA_ROOT}')
print(f'MEDIA_URL: {settings.MEDIA_URL}')
PYEOF
echo ''

echo "=== 업로드된 파일 찾기 ==="
find /home/ubuntu/planit -name '*.JPG' -o -name '*.jpg' -o -name '*.png' 2>/dev/null | head -20
echo ''

echo "=== nginx media 설정 확인 ==="
grep -A 3 "location /media/" /etc/nginx/sites-enabled/planit 2>/dev/null || echo 'nginx 설정 파일 없음'
