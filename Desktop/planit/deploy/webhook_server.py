#!/usr/bin/env python3
"""
GitHub Webhook을 받아서 자동 배포하는 서버
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import subprocess
import os
import hashlib
import hmac

# 설정
WEBHOOK_SECRET = "your_webhook_secret_here"  # GitHub에서 설정한 시크릿
DEPLOY_SCRIPT = "/home/ubuntu/planit/deploy/auto_deploy.sh"

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/webhook':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # GitHub 시그니처 검증 (보안)
            signature = self.headers.get('X-Hub-Signature-256')
            if signature and self.verify_signature(post_data, signature):
                try:
                    payload = json.loads(post_data.decode('utf-8'))
                    
                    # main 브랜치에 푸시된 경우에만 배포
                    if (payload.get('ref') == 'refs/heads/main' and 
                        payload.get('repository', {}).get('name') == 'planit'):
                        
                        print("🚀 GitHub에서 main 브랜치 푸시 감지! 자동 배포 시작...")
                        
                        # 배포 스크립트 실행
                        result = subprocess.run(['/bin/bash', DEPLOY_SCRIPT], 
                                              capture_output=True, text=True)
                        
                        if result.returncode == 0:
                            print("✅ 자동 배포 성공!")
                            self.send_response(200)
                            self.send_header('Content-type', 'text/plain')
                            self.end_headers()
                            self.wfile.write(b'Deployment successful')
                        else:
                            print(f"❌ 배포 실패: {result.stderr}")
                            self.send_response(500)
                            self.send_header('Content-type', 'text/plain')
                            self.end_headers()
                            self.wfile.write(b'Deployment failed')
                    else:
                        self.send_response(200)
                        self.send_header('Content-type', 'text/plain')
                        self.end_headers()
                        self.wfile.write(b'Not a main branch push')
                        
                except Exception as e:
                    print(f"❌ 웹훅 처리 오류: {e}")
                    self.send_response(500)
                    self.send_header('Content-type', 'text/plain')
                    self.end_headers()
                    self.wfile.write(b'Webhook processing failed')
            else:
                self.send_response(403)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Invalid signature')
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not found')
    
    def verify_signature(self, payload, signature):
        """GitHub 웹훅 시그니처 검증"""
        if not WEBHOOK_SECRET:
            return True  # 시크릿이 없으면 검증 생략
            
        expected_signature = 'sha256=' + hmac.new(
            WEBHOOK_SECRET.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(expected_signature, signature)

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 9000), WebhookHandler)
    print("🎯 GitHub Webhook 서버 시작 (포트 9000)")
    print("📡 웹훅 URL: http://your-server:9000/webhook")
    server.serve_forever()
