#!/usr/bin/env python
"""
실제 브라우저 환경을 시뮬레이션하는 테스트
"""
import os
import django
import requests
import sys
from urllib.parse import urljoin

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.development')
django.setup()

from accounts.models import User

def simulate_browser_registration():
    """실제 브라우저 환경 시뮬레이션"""
    
    base_url = 'http://127.0.0.1:8000'
    
    # 브라우저와 유사한 헤더 설정
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ko-KR,ko;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
    try:
        print("=== 브라우저 시뮬레이션 테스트 시작 ===")
        
        # 1. 홈페이지 접근 (쿠키 설정)
        print("1. 홈페이지 접근...")
        response = session.get(base_url)
        print(f"홈페이지 응답: {response.status_code}")
        
        # 2. 회원가입 페이지 GET
        print("2. 회원가입 페이지 접근...")
        register_url = urljoin(base_url, '/accounts/register/')
        response = session.get(register_url)
        print(f"회원가입 페이지 응답: {response.status_code}")
        
        if response.status_code != 200:
            print(f"회원가입 페이지 접근 실패!")
            return False
        
        # 3. CSRF 토큰 추출
        import re
        csrf_token = None
        csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
        if csrf_match:
            csrf_token = csrf_match.group(1)
            print(f"CSRF 토큰: {csrf_token[:20]}...")
        else:
            print("CSRF 토큰을 찾을 수 없습니다!")
            return False
        
        # 4. 테스트 사용자 정리
        User.objects.filter(username='realtest').delete()
        User.objects.filter(student_id='2024888').delete()
        
        # 5. 회원가입 데이터 (실제 브라우저에서 보내는 형태)
        form_data = {
            'csrfmiddlewaretoken': csrf_token,
            'username': 'realtest',
            'first_name': '실제',
            'last_name': '테스트',
            'email': 'real@test.com',
            'student_id': '2024888',
            'department': 'COMP',
            'grade': '1',
            'phone_number': '',  # 빈 값
            'password1': 'testpass123!',
            'password2': 'testpass123!',
        }
        
        # 6. POST 요청 (브라우저와 동일한 헤더)
        print("3. 회원가입 POST 요청...")
        post_headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': register_url,
            'Origin': base_url,
        }
        
        response = session.post(register_url, data=form_data, headers=post_headers, allow_redirects=False)
        print(f"POST 응답 코드: {response.status_code}")
        print(f"응답 헤더: {dict(response.headers)}")
        
        if response.status_code == 302:
            print("✓ 회원가입 성공 (리다이렉트)")
            print(f"리다이렉트 위치: {response.headers.get('Location', 'N/A')}")
            
            # 사용자 확인
            try:
                user = User.objects.get(username='realtest')
                print(f"✓ 사용자 생성 확인: {user.username} ({user.student_id})")
                return True
            except User.DoesNotExist:
                print("✗ 사용자가 생성되지 않았습니다!")
                return False
                
        elif response.status_code == 200:
            print("✗ 폼 오류 (200 응답)")
            # 오류 메시지 찾기
            error_patterns = [
                r'<div class="alert alert-danger"[^>]*>(.*?)</div>',
                r'<ul class="errorlist"[^>]*>(.*?)</ul>',
                r'class="invalid-feedback"[^>]*>(.*?)</div>',
            ]
            
            for pattern in error_patterns:
                matches = re.findall(pattern, response.text, re.DOTALL | re.IGNORECASE)
                if matches:
                    print(f"오류 메시지 발견: {matches}")
            
            return False
            
        elif response.status_code == 500:
            print("✗ 서버 오류 (500)")
            print(f"오류 내용: {response.text[:1000]}")
            return False
            
        else:
            print(f"✗ 예상치 못한 응답: {response.status_code}")
            print(f"응답 내용: {response.text[:500]}")
            return False
            
    except Exception as e:
        print(f"✗ 테스트 중 예외 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # 정리
        try:
            User.objects.filter(username='realtest').delete()
        except:
            pass

if __name__ == '__main__':
    success = simulate_browser_registration()
    print(f"\n최종 결과: {'성공' if success else '실패'}")
    sys.exit(0 if success else 1)
