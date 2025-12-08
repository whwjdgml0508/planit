#!/usr/bin/env python
"""
실시간 회원가입 디버깅 스크립트
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
import traceback

def debug_registration():
    """회원가입 디버깅"""
    client = Client()
    
    # 다양한 테스트 케이스
    test_cases = [
        {
            'name': '정상 케이스',
            'data': {
                'username': 'normaluser',
                'first_name': '정상',
                'last_name': '사용자',
                'email': 'normal@test.com',
                'student_id': '2024001',
                'department': 'COMP',
                'grade': '1',
                'phone_number': '',
                'password1': 'testpass123!',
                'password2': 'testpass123!',
            }
        },
        {
            'name': '전화번호 포함 케이스',
            'data': {
                'username': 'phoneuser',
                'first_name': '전화',
                'last_name': '사용자',
                'email': 'phone@test.com',
                'student_id': '2024002',
                'department': 'COMP',
                'grade': '2',
                'phone_number': '010-1234-5678',
                'password1': 'testpass123!',
                'password2': 'testpass123!',
            }
        },
        {
            'name': '잘못된 전화번호 케이스',
            'data': {
                'username': 'badphone',
                'first_name': '잘못된',
                'last_name': '전화번호',
                'email': 'badphone@test.com',
                'student_id': '2024003',
                'department': 'COMP',
                'grade': '3',
                'phone_number': '01012345678',  # 하이픈 없음
                'password1': 'testpass123!',
                'password2': 'testpass123!',
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n=== {test_case['name']} 테스트 ===")
        try:
            # 기존 사용자 삭제
            User.objects.filter(username=test_case['data']['username']).delete()
            User.objects.filter(student_id=test_case['data']['student_id']).delete()
            
            # 회원가입 시도
            print(f"테스트 데이터: {test_case['data']}")
            response = client.post(reverse('accounts:register'), test_case['data'])
            
            print(f"응답 코드: {response.status_code}")
            
            if response.status_code == 302:
                print("[SUCCESS] 회원가입 성공")
                user = User.objects.get(username=test_case['data']['username'])
                print(f"생성된 사용자: {user.username} ({user.student_id})")
            elif response.status_code == 200:
                print("[WARNING] 폼 오류 발생")
                if hasattr(response, 'context') and 'form' in response.context:
                    form = response.context['form']
                    if form.errors:
                        print(f"폼 오류: {form.errors}")
                    if form.non_field_errors():
                        print(f"일반 오류: {form.non_field_errors()}")
            else:
                print(f"[ERROR] 예상치 못한 응답: {response.status_code}")
                print(f"응답 내용 (처음 500자): {response.content[:500]}")
                
        except Exception as e:
            print(f"[ERROR] 예외 발생: {str(e)}")
            traceback.print_exc()
        
        finally:
            # 정리
            try:
                User.objects.filter(username=test_case['data']['username']).delete()
            except:
                pass

if __name__ == '__main__':
    debug_registration()
