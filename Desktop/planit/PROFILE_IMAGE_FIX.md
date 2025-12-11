# 프로필 이미지 업로드 및 표시 수정 완료

## 문제 상황
프로필 사진을 업로드하고 저장해도 프로필 사진이 표시되지 않는 문제 발생

## 원인 분석

### 1. **View 레벨 문제**
- `ProfileEditView`에서 파일 업로드를 명시적으로 처리하지 않음
- `form.save()`만 호출하여 `request.FILES`가 제대로 처리되지 않음

### 2. **템플릿 레벨 문제**
- `get_avatar_url()` 메서드가 프로필 이미지 URL과 이모지를 모두 반환
- 일부 템플릿에서 `<span>` 태그 안에 URL을 넣어 이미지가 표시되지 않음

## 수정 사항

### 1. **accounts/views.py - ProfileEditView 수정**
```python
def form_valid(self, form):
    user = form.save(commit=False)
    
    # 프로필 이미지 삭제 처리
    if self.request.POST.get('profile_image-clear') == 'on':
        if user.profile_image:
            user.profile_image.delete(save=False)
            user.profile_image = None
        user.save()
        messages.success(self.request, '프로필 이미지가 제거되었습니다.')
        logger.info(f"프로필 이미지 제거 - 사용자: {user.username}")
        return redirect(self.success_url)
    
    # 새 프로필 이미지 업로드 처리
    if 'profile_image' in self.request.FILES:
        # 기존 이미지가 있으면 삭제
        if user.profile_image:
            user.profile_image.delete(save=False)
        user.profile_image = self.request.FILES['profile_image']
        logger.info(f"프로필 이미지 업로드 - 사용자: {user.username}, 파일: {user.profile_image.name}")
    
    user.save()
    messages.success(self.request, '프로필이 성공적으로 업데이트되었습니다.')
    logger.info(f"프로필 업데이트 성공 - 사용자: {user.username}")
    return redirect(self.success_url)
```

**주요 개선점:**
- `request.FILES`에서 파일을 명시적으로 가져와 처리
- 기존 이미지 자동 삭제 후 새 이미지로 교체
- 상세한 로깅 추가로 디버깅 가능

### 2. **accounts/models.py - User 모델에 메서드 추가**
```python
def get_avatar_emoji(self):
    """아바타 이모지만 반환 (프로필 이미지 무시)"""
    avatar_map = {
        'default': '👤',
        'student_male': '👨‍🎓',
        'student_female': '👩‍🎓',
        'soldier': '🪖',
        'pilot': '👨‍✈️',
        'engineer': '👨‍🔧',
        'scientist': '👨‍🔬',
        'astronaut': '👨‍🚀',
    }
    return avatar_map.get(self.avatar_choice, '👤')
```

**목적:**
- 프로필 이미지가 없을 때만 이모지를 반환하는 전용 메서드
- `get_avatar_url()`은 하위 호환성을 위해 유지

### 3. **템플릿 수정 - 모든 위치에서 일관된 패턴 사용**

수정된 템플릿:
- `templates/base.html` - 네비게이션 바
- `templates/community/index.html` - 커뮤니티 메인
- `templates/community/post_list.html` - 게시글 목록
- `templates/community/post_detail.html` - 게시글 상세, 댓글, 답글

**일관된 패턴:**
```django
{% if user.profile_image %}
    <img src="{{ user.profile_image.url }}" alt="프로필" class="rounded-circle" width="X" height="X" style="object-fit: cover;">
{% else %}
    <span style="font-size: Xpx;">{{ user.get_avatar_emoji }}</span>
{% endif %}
```

### 4. **Media 디렉토리 권한 설정**

배포 스크립트에서 자동으로 처리:
```bash
sudo mkdir -p /var/www/planit/media/profiles
sudo chown -R ubuntu:www-data /var/www/planit/media
sudo chmod -R 775 /var/www/planit/media
```

## 배포 방법

### PowerShell에서 실행:
```powershell
.\deploy_profile_image_fix.ps1
```

### 수동 배포:
```bash
# 1. 코드 업데이트
ssh -i ~/.ssh/ec2-kafa-2-key.pem ubuntu@35.163.12.109
cd /home/ubuntu/planit
git pull origin main

# 2. Media 디렉토리 권한 설정
sudo mkdir -p /var/www/planit/media/profiles
sudo chown -R ubuntu:www-data /var/www/planit/media
sudo chmod -R 775 /var/www/planit/media

# 3. 서비스 재시작
sudo systemctl restart planit
sudo systemctl status planit
```

## 테스트 방법

1. **프로필 이미지 업로드 테스트**
   - http://planit.boramae.club/accounts/profile/ 접속
   - "프로필 수정" 버튼 클릭
   - 이미지 파일 선택 및 업로드
   - "프로필 업데이트" 버튼 클릭

2. **표시 확인 위치**
   - ✅ 프로필 페이지 (100x100)
   - ✅ 네비게이션 바 드롭다운 (32x32)
   - ✅ 커뮤니티 인덱스 - 공지사항 (40x40)
   - ✅ 커뮤니티 인덱스 - 최근 게시글 (40x40)
   - ✅ 게시글 목록 (32x32)
   - ✅ 게시글 상세 - 작성자 (40x40)
   - ✅ 게시글 상세 - 댓글 (40x40)
   - ✅ 게시글 상세 - 답글 (32x32)
   - ✅ 게시글 상세 - 작성자 정보 카드 (80x80)

3. **이미지 제거 테스트**
   - 프로필 수정 페이지에서 "현재 프로필 이미지 제거" 체크
   - 저장 후 선택한 아바타 이모지가 표시되는지 확인

## 기술적 세부사항

### 파일 업로드 처리
- Django의 `request.FILES`를 통해 파일 접근
- `ImageField`는 자동으로 `MEDIA_ROOT/profiles/` 경로에 저장
- 기존 파일은 `delete(save=False)`로 삭제 후 새 파일 할당

### 이미지 표시
- `profile_image.url`은 `/media/profiles/filename.jpg` 형식 반환
- Nginx가 `/media/` 경로를 `/var/www/planit/media/`로 매핑
- `object-fit: cover`로 원형 이미지 내 비율 유지

### 권한 설정
- 소유자: `ubuntu` (Django 프로세스 실행 사용자)
- 그룹: `www-data` (Nginx 실행 그룹)
- 권한: `775` (소유자/그룹 읽기+쓰기+실행, 기타 읽기+실행)

## 로그 확인

### Django 로그:
```bash
sudo journalctl -u planit -f
```

### Nginx 로그:
```bash
sudo tail -f /var/log/nginx/planit_access.log
sudo tail -f /var/log/nginx/planit_error.log
```

## 문제 해결

### 이미지가 여전히 표시되지 않는 경우:

1. **권한 확인**
   ```bash
   ls -la /var/www/planit/media/profiles/
   ```

2. **파일 존재 확인**
   ```bash
   find /var/www/planit/media -type f -name "*.jpg" -o -name "*.png"
   ```

3. **Django 로그 확인**
   ```bash
   sudo journalctl -u planit -n 50 | grep profile_image
   ```

4. **Nginx 설정 확인**
   ```bash
   sudo nginx -t
   cat /etc/nginx/sites-enabled/planit
   ```

## 완료 체크리스트

- [x] ProfileEditView 파일 업로드 처리 수정
- [x] User 모델에 get_avatar_emoji() 메서드 추가
- [x] 모든 템플릿에서 일관된 패턴 사용
- [x] Media 디렉토리 권한 설정 스크립트 작성
- [x] 배포 스크립트 작성
- [ ] Production 서버 배포
- [ ] 실제 이미지 업로드 및 표시 테스트

## 다음 단계

1. `deploy_profile_image_fix.ps1` 실행하여 배포
2. 실제 프로필 이미지 업로드 테스트
3. 모든 페이지에서 이미지 표시 확인
4. 문제 발생 시 로그 확인 및 디버깅
