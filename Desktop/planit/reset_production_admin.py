#!/usr/bin/env python
import os
import django

# Production Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.production')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

print("=== Production Admin 비밀번호 재설정 ===")

try:
    admin = User.objects.get(username='admin')
    
    # 새 비밀번호 설정
    new_password = 'admin123'
    admin.set_password(new_password)
    admin.save()
    
    print(f"✅ Admin 비밀번호가 '{new_password}'로 재설정되었습니다.")
    
    # 비밀번호 확인
    if admin.check_password(new_password):
        print("✅ 비밀번호 재설정 확인 완료")
    else:
        print("❌ 비밀번호 재설정 실패")
    
    print(f"\n로그인 정보:")
    print(f"- 사용자명: admin")
    print(f"- 비밀번호: {new_password}")
    print(f"- URL: http://planit.boramae.club/accounts/login/")
    
except User.DoesNotExist:
    print("❌ Admin 계정이 존재하지 않습니다.")
except Exception as e:
    print(f"❌ 오류 발생: {e}")
