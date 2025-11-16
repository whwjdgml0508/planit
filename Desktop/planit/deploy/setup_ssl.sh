#!/bin/bash

# PlanIt HTTPS 설정 스크립트 (Let's Encrypt)

echo "🔒 PlanIt HTTPS 설정을 시작합니다..."

# 도메인 설정
DOMAIN="planit.boramae.club"
EMAIL="admin@boramae.club"  # 실제 이메일로 변경 필요

# Certbot 설치 확인
if ! command -v certbot &> /dev/null; then
    echo "📦 Certbot 설치 중..."
    sudo apt update
    sudo apt install -y certbot python3-certbot-nginx
fi

# Nginx 설정 백업
echo "💾 기존 Nginx 설정 백업 중..."
sudo cp /etc/nginx/sites-available/planit /etc/nginx/sites-available/planit.backup.$(date +%Y%m%d_%H%M%S)

# SSL 인증서 발급
echo "🔐 SSL 인증서 발급 중..."
sudo certbot --nginx -d $DOMAIN --email $EMAIL --agree-tos --non-interactive

# 자동 갱신 설정
echo "🔄 SSL 인증서 자동 갱신 설정 중..."
sudo crontab -l | grep -q "certbot renew" || (sudo crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet") | sudo crontab -

# Nginx 재시작
echo "🔄 Nginx 재시작 중..."
sudo systemctl restart nginx

# 방화벽 설정 (HTTPS 포트 443 열기)
echo "🛡️ 방화벽 설정 중..."
sudo ufw allow 443/tcp

# SSL 설정 확인
echo "✅ SSL 설정 확인 중..."
if curl -s -I https://$DOMAIN | grep -q "200 OK"; then
    echo "🎉 HTTPS 설정이 완료되었습니다!"
    echo "🌐 접속 주소: https://$DOMAIN"
else
    echo "❌ HTTPS 설정에 문제가 있습니다. 로그를 확인해주세요."
    sudo nginx -t
    sudo systemctl status nginx
fi

echo "📋 SSL 인증서 정보:"
sudo certbot certificates

echo "🔒 HTTPS 설정 완료!"
