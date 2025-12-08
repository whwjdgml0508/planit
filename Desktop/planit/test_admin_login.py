#!/usr/bin/env python
import os
import django

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.development')
django.setup()

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()

# 로그인 테스트
username = 'admin'
password = 'admin123'

print(f"로그인 테스트: {username} / {password}")

# Django 인증 시스템을 통한 로그인 테스트
user = authenticate(username=username, password=password)

if user is not None:
    if user.is_active:
        print("SUCCESS: 로그인 성공!")
        print(f"- 사용자: {user.username}")
        print(f"- 이메일: {user.email}")
        print(f"- 슈퍼유저: {user.is_superuser}")
        print(f"- 스태프: {user.is_staff}")
    else:
        print("ERROR: 계정이 비활성화되어 있습니다.")
else:
    print("ERROR: 로그인 실패 - 사용자명 또는 비밀번호가 잘못되었습니다.")

# 커스텀 백엔드 테스트
from accounts.backends import StudentIdBackend

backend = StudentIdBackend()
user_backend = backend.authenticate(None, username=username, password=password)

if user_backend:
    print("커스텀 백엔드를 통한 로그인도 성공!")
else:
    print("커스텀 백엔드를 통한 로그인 실패")
