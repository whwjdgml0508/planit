# Screenshots Guide

## 📸 스크린샷 촬영 가이드

이 폴더에는 README.md에서 참조하는 애플리케이션 스크린샷들이 저장됩니다.

### 필요한 스크린샷 목록:

1. **main_page.png** - 메인 페이지 대시보드
   - URL: http://planit.boramae.club/
   - 포함 요소: 네비게이션, 시간표 미리보기, 플래너 요약

2. **timetable.png** - 시간표 관리 페이지
   - URL: http://planit.boramae.club/timetable/
   - 포함 요소: 시간표 그리드, 편집 기능

3. **planner.png** - 스터디 플래너 페이지
   - URL: http://planit.boramae.club/planner/
   - 포함 요소: 학습 계획, 진도 관리

4. **community.png** - 커뮤니티 페이지
   - URL: http://planit.boramae.club/community/
   - 포함 요소: 게시글 목록, 카테고리

5. **mobile_app.png** - 모바일 앱 화면
   - 안드로이드 앱 실행 화면 또는 모바일 반응형 웹

6. **admin_page.png** - 관리자 페이지
   - URL: http://planit.boramae.club/admin/
   - Django 관리자 인터페이스

### 스크린샷 촬영 방법:

1. **웹 브라우저에서 촬영**:
   - 브라우저 개발자 도구로 모바일 뷰 시뮬레이션
   - 전체 페이지 스크린샷 (F12 → Ctrl+Shift+P → "screenshot")

2. **권장 해상도**:
   - 데스크톱: 1920x1080
   - 모바일: 375x667 (iPhone SE) 또는 360x640 (Android)

3. **파일 형식**: PNG (고품질, 투명 배경 지원)

### 자동 스크린샷 도구 (선택사항):

```bash
# Playwright를 사용한 자동 스크린샷
pip install playwright
python take_screenshots.py
```

### 주의사항:
- 개인정보가 포함된 화면은 모자이크 처리
- 테스트 데이터 사용 권장
- 일관된 브라우저 및 해상도 사용
