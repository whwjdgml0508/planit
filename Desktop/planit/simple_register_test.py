#!/usr/bin/env python
"""
간단한 회원가입 테스트 - 브라우저와 동일한 환경
"""
import os
import django
import requests
import sys

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.development')
django.setup()

from django.test import Client
from django.urls import reverse
from accounts.models import User

def test_browser_like_registration():
    """브라우저와 유사한 회원가입 테스트"""
    
    # 실제 서버에 요청
    base_url = 'http://127.0.0.1:8000'
    
    try:
        # 1. 회원가입 페이지 GET 요청
        print("1. 회원가입 페이지 접근 중...")
        session = requests.Session()
        response = session.get(f'{base_url}/accounts/register/')
        print(f"GET 응답 코드: {response.status_code}")
        
        if response.status_code != 200:
            print(f"회원가입 페이지 접근 실패: {response.status_code}")
            print(f"응답 내용: {response.text[:500]}")
            return False
        
        # 2. CSRF 토큰 추출
        csrf_token = None
        if 'csrfmiddlewaretoken' in response.text:
            import re
            csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
            if csrf_match:
                csrf_token = csrf_match.group(1)
                print(f"CSRF 토큰 추출: {csrf_token[:20]}...")
        
        if not csrf_token:
            print("CSRF 토큰을 찾을 수 없습니다!")
            return False
        
        # 3. 회원가입 데이터 준비
        form_data = {
            'csrfmiddlewaretoken': csrf_token,
            'username': 'browsertest',
            'first_name': '브라우저',
            'last_name': '테스트',
            'email': 'browser@test.com',
            'student_id': '2024999',
            'department': 'COMP',
            'grade': '1',
            'phone_number': '',
            'password1': 'testpass123!',
            'password2': 'testpass123!',
        }
        
        # 기존 사용자 삭제
        User.objects.filter(username='browsertest').delete()
        User.objects.filter(student_id='2024999').delete()
        
        # 4. POST 요청
        print("2. 회원가입 POST 요청 중...")
        response = session.post(f'{base_url}/accounts/register/', data=form_data)
        print(f"POST 응답 코드: {response.status_code}")
        print(f"응답 URL: {response.url}")
        
        if response.status_code == 200:
            print("폼 오류가 있을 수 있습니다.")
            # 오류 메시지 찾기
            if 'error' in response.text.lower() or 'invalid' in response.text.lower():
                print("응답에 오류 메시지가 포함되어 있습니다:")
                print(response.text[:1000])
        elif response.status_code == 302:
            print("회원가입 성공 (리다이렉트)")
        elif response.status_code == 500:
            print("서버 오류 발생!")
            print(f"오류 응답: {response.text[:1000]}")
        else:
            print(f"예상치 못한 응답: {response.status_code}")
            print(f"응답 내용: {response.text[:500]}")
        
        return response.status_code in [200, 302]
        
    except Exception as e:
        print(f"요청 중 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # 정리
        try:
            User.objects.filter(username='browsertest').delete()
        except:
            pass

if __name__ == '__main__':
    success = test_browser_like_registration()
    print(f"\n테스트 결과: {'성공' if success else '실패'}")
