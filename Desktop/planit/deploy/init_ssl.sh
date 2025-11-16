#!/bin/bash

# SSL 인증서 초기 발급 스크립트 (Docker 환경용)

DOMAIN="planit.boramae.club"
EMAIL="admin@boramae.club"  # 실제 이메일로 변경 필요

echo "🔒 SSL 인증서 초기 발급을 시작합니다..."

# 임시 nginx 설정으로 HTTP 서버 시작
echo "📝 임시 nginx 설정 생성 중..."
cat > /tmp/nginx_temp.conf << EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
    
    location / {
        return 200 'OK';
        add_header Content-Type text/plain;
    }
}
EOF

# Docker Compose로 임시 서버 시작
echo "🚀 임시 웹서버 시작 중..."
docker-compose -f docker-compose.prod.yml up -d nginx

# Certbot으로 인증서 발급
echo "🔐 SSL 인증서 발급 중..."
docker-compose -f docker-compose.prod.yml run --rm certbot \
    certonly --webroot --webroot-path /var/www/certbot \
    --email $EMAIL --agree-tos --no-eff-email \
    -d $DOMAIN -d www.$DOMAIN

# 인증서 발급 확인
if [ -f "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ]; then
    echo "✅ SSL 인증서 발급 완료!"
    
    # HTTPS 설정으로 nginx 재시작
    echo "🔄 HTTPS 설정으로 nginx 재시작 중..."
    docker-compose -f docker-compose.prod.yml restart nginx
    
    echo "🎉 HTTPS 설정이 완료되었습니다!"
    echo "🌐 접속 주소: https://$DOMAIN"
else
    echo "❌ SSL 인증서 발급에 실패했습니다."
    echo "도메인 DNS 설정을 확인해주세요."
fi
