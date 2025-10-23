#!/bin/bash
echo "🔧 템플릿 static 태그 오류 수정 중..."

# 서버로 이동
cd /home/ubuntu/planit

# 가상환경 활성화
source /home/ubuntu/planit/planit/venv/bin/activate

# base.html 파일 확인 및 수정
echo "📝 base.html 파일 확인 중..."

# base.html 파일의 첫 번째 줄이 {% load static %}인지 확인
FIRST_LINE=$(head -n 1 templates/base.html)

if [[ "$FIRST_LINE" != "{% load static %}" ]]; then
    echo "❌ base.html 파일에 {% load static %} 태그가 없습니다. 수정 중..."
    
    # 백업 생성
    cp templates/base.html templates/base.html.backup
    
    # 임시 파일 생성하여 {% load static %}를 맨 위에 추가
    echo "{% load static %}" > templates/base.html.tmp
    cat templates/base.html >> templates/base.html.tmp
    mv templates/base.html.tmp templates/base.html
    
    echo "✅ base.html 파일이 수정되었습니다."
else
    echo "✅ base.html 파일이 이미 올바릅니다."
fi

# 정적 파일 다시 수집
echo "📁 정적 파일 재수집 중..."
python manage.py collectstatic --noinput

# 서버 재시작
echo "🔄 서버 재시작 중..."
pkill -f python
pkill -f gunicorn
nohup python manage.py runserver 127.0.0.1:8000 > server.log 2>&1 &

echo "✅ 템플릿 static 태그 오류 수정 완료!"
echo "🌐 사이트를 다시 확인해보세요: http://planit.boramae.club/"
