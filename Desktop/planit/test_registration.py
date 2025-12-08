#!/usr/bin/env python
"""
회원가입 테스트 스크립트
"""
import os
import django
import sys

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.development')
django.setup()

from django.test import Client
from django.urls import reverse
from accounts.models import User

def test_registration():
    """회원가입 테스트"""
    client = Client()
    
    # 테스트 데이터
    test_data = {
        'username': 'testuser123',
        'first_name': '테스트',
        'last_name': '사용자',
        'email': 'test@example.com',
        'student_id': '1234567',
        'department': 'COMP',
        'grade': '2',
        'phone_number': '',  # 빈 값으로 테스트
        'password1': 'testpass123!',
        'password2': 'testpass123!',
    }
    
    print("회원가입 테스트 시작...")
    print(f"테스트 데이터: {test_data}")
    
    try:
        # 기존 테스트 사용자 삭제 (있다면)
        User.objects.filter(username='testuser123').delete()
        User.objects.filter(student_id='1234567').delete()
        print("기존 테스트 사용자 삭제 완료")
        
        # 회원가입 페이지 접근
        response = client.get(reverse('accounts:register'))
        print(f"회원가입 페이지 접근: {response.status_code}")
        
        if response.status_code != 200:
            print(f"회원가입 페이지 접근 실패: {response.status_code}")
            return False
        
        # 회원가입 POST 요청
        response = client.post(reverse('accounts:register'), test_data)
        print(f"회원가입 POST 응답: {response.status_code}")
        
        if response.status_code == 302:
            print("[SUCCESS] 회원가입 성공 (리다이렉트)")
            # 사용자가 생성되었는지 확인
            user = User.objects.get(username='testuser123')
            print(f"[SUCCESS] 사용자 생성 확인: {user.username} ({user.student_id})")
            return True
        elif response.status_code == 200:
            print("[ERROR] 회원가입 실패 (폼 오류)")
            # 폼 오류 확인
            if hasattr(response, 'context') and 'form' in response.context:
                form = response.context['form']
                if form.errors:
                    print(f"폼 오류: {form.errors}")
            return False
        else:
            print(f"[ERROR] 예상치 못한 응답 코드: {response.status_code}")
            print(f"응답 내용: {response.content[:500]}")
            return False
            
    except Exception as e:
        print(f"[ERROR] 테스트 중 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # 테스트 사용자 정리
        try:
            User.objects.filter(username='testuser123').delete()
            print("테스트 사용자 정리 완료")
        except:
            pass

if __name__ == '__main__':
    success = test_registration()
    sys.exit(0 if success else 1)
