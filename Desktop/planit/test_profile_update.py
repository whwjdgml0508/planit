"""
프로필 업데이트 기능 테스트 스크립트
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.development')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

def test_profile_update():
    """프로필 업데이트 테스트"""
    
    # 테스트 사용자 생성 또는 가져오기
    try:
        user = User.objects.get(username='admin')
        print(f"✓ 기존 사용자 사용: {user.username}")
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            student_id='1234567',
            first_name='테스트',
            last_name='사용자',
            department='COMP',
            grade=1
        )
        print(f"✓ 새 테스트 사용자 생성: {user.username}")
    
    # 클라이언트 생성 및 로그인
    client = Client()
    login_success = client.login(username=user.username, password='admin123' if user.username == 'admin' else 'testpass123')
    
    if not login_success:
        print("✗ 로그인 실패")
        return False
    
    print(f"✓ 로그인 성공: {user.username}")
    
    # 프로필 수정 페이지 GET 요청
    profile_edit_url = reverse('accounts:profile_edit')
    response = client.get(profile_edit_url)
    
    print(f"\n프로필 수정 페이지 GET 요청:")
    print(f"  - URL: {profile_edit_url}")
    print(f"  - Status Code: {response.status_code}")
    
    if response.status_code != 200:
        print(f"✗ 프로필 수정 페이지 로드 실패")
        print(f"  - Response: {response.content[:500]}")
        return False
    
    print(f"✓ 프로필 수정 페이지 로드 성공")
    
    # 프로필 업데이트 POST 요청
    update_data = {
        'first_name': '업데이트',
        'last_name': '테스트',
        'email': user.email,
        'department': 'COMP',
        'grade': 2,
        'phone_number': '010-1234-5678',
        'avatar_choice': 'student_male',
        'bio': '프로필 업데이트 테스트입니다.'
    }
    
    response = client.post(profile_edit_url, update_data)
    
    print(f"\n프로필 업데이트 POST 요청:")
    print(f"  - Status Code: {response.status_code}")
    
    if response.status_code == 500:
        print(f"✗ 서버 에러 발생 (500)")
        return False
    
    if response.status_code == 302:
        print(f"✓ 리다이렉트 성공 (302)")
        print(f"  - Redirect URL: {response.url}")
    
    # 업데이트된 데이터 확인
    user.refresh_from_db()
    print(f"\n업데이트된 프로필:")
    print(f"  - 이름: {user.last_name}{user.first_name}")
    print(f"  - 학년: {user.grade}학년")
    print(f"  - 전화번호: {user.phone_number}")
    print(f"  - 아바타: {user.avatar_choice}")
    print(f"  - 자기소개: {user.bio}")
    
    if user.first_name == '업데이트' and user.grade == 2:
        print(f"\n✓ 프로필 업데이트 성공!")
        return True
    else:
        print(f"\n✗ 프로필 업데이트 실패 - 데이터가 저장되지 않음")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("프로필 업데이트 기능 테스트")
    print("=" * 60)
    
    try:
        success = test_profile_update()
        print("\n" + "=" * 60)
        if success:
            print("테스트 결과: 성공 ✓")
        else:
            print("테스트 결과: 실패 ✗")
        print("=" * 60)
    except Exception as e:
        print(f"\n✗ 테스트 중 오류 발생:")
        print(f"  - {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
