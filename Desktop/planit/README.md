# PlanIt - 생도 학습 관리 플랫폼

## 프로젝트 개요
학습 데이터를 통합하고 학과 커뮤니티를 연계하여 생도 생활의 효율성과 소통을 강화하는 **크로스 플랫폼 애플리케이션**

## 주요 기능

### 1. 스터디 플래너 및 학습 진도 관리
- 수정 가능한 시간표
- 각 과목별 평가 방식 기록
- 스터디 플래너 기능
- 학습 진도 추적
- 일일 계획 및 목표 설정

### 2. 커뮤니티 기능
- 학과별 소통 공간
- 시험 자료 공유
- 강의 특성 정보 공유
- 체력평가 팁 커뮤니티
- 영어 상식 공유

### 3. 통합 정보 관리
- E-class와 구글 클래스 정보 통합
- 강의계획서 관리
- 평가 정보 통합

### 4. 크로스 플랫폼 지원 🆕
- **웹 애플리케이션**: 반응형 웹 디자인
- **Android 앱**: WebView 기반 네이티브 앱
- **Windows 데스크톱**: Electron 기반 데스크톱 앱
- **모바일 최적화**: Cordova 기반 하이브리드 앱

## 기술 스택
- **Backend**: Django 5.2.7
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (개발용), MySQL (배포용)
- **UI Framework**: Bootstrap 5 + Crispy Forms
- **웹서버**: Nginx
- **WSGI**: Gunicorn
- **배포**: AWS EC2 (Ubuntu 22.04)
- **도메인**: http://planit.boramae.club ✅ **배포 완료**
- **모바일**: Android Studio, Cordova, WebView
- **데스크톱**: Electron, Python (tkinter/PyQt)
- **빌드 도구**: Gradle, npm, Python setuptools

## 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/whwjdgml0508/cadet-learning-platform.git
cd planit
```

### 2. 가상환경 생성 및 활성화 (선택사항)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. 패키지 설치
```bash
pip install -r requirements.txt
```

### 4. 데이터베이스 마이그레이션
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. 슈퍼유저 생성 (선택사항)
```bash
python manage.py createsuperuser
```

### 6. 개발 서버 실행
```bash
python manage.py runserver
```

브라우저에서 `http://127.0.0.1:8000`으로 접속하여 확인할 수 있습니다.

## 📱 모바일 및 데스크톱 앱 빌드

### Android APK 빌드
```bash
# 기본 APK 빌드
python create_perfect_apk.py

# 최소 버전 APK 빌드
python create_minimal_apk.py

# WebView 기반 APK 빌드
python create_webview_apk.py

# 실제 배포용 APK 빌드
python create_real_android_apk.py
```

### Windows EXE 빌드
```bash
# Windows 실행 파일 생성
python create_windows_exe.py
```

### 통합 빌드
```bash
# 모든 플랫폼 앱 빌드
python build_real_apps.py

# 기본 앱들 빌드
python build_apps.py
```

### 📥 빌드된 앱 다운로드
빌드가 완료된 앱들은 `downloads/` 폴더에서 다운로드할 수 있습니다:
- `downloads/planit.apk` - Android 앱
- `downloads/planit.exe` - Windows 데스크톱 앱
- `downloads/README.md` - 다운로드 가이드

## 프로젝트 구조
```
planit/
├── accounts/           # 사용자 인증 및 프로필 관리
├── timetable/          # 시간표 관리
├── planner/            # 학습 플래너
├── community/          # 커뮤니티 기능
├── templates/          # HTML 템플릿
├── static/             # 정적 파일 (CSS, JS, 이미지)
├── media/              # 업로드된 파일
├── planit_project/     # Django 프로젝트 설정
├── mobile/             # 모바일 앱 개발 🆕
│   ├── android/        # Android 네이티브 앱
│   └── cordova/        # Cordova 하이브리드 앱
├── desktop/            # 데스크톱 앱 개발 🆕
│   ├── electron/       # Electron 앱
│   └── src/            # 데스크톱 앱 소스
├── deploy/             # 배포 관련 파일들
├── downloads/          # 빌드된 앱 다운로드
├── build_*.py          # 앱 빌드 스크립트들 🆕
├── create_*.py         # 앱 생성 스크립트들 🆕
├── manage.py
├── requirements.txt
└── README.md
```

## 📸 화면 캡처

### 메인 페이지
![메인 페이지](screenshots/main_page.png)
*PlanIt 메인 대시보드 - 시간표와 플래너가 통합된 인터페이스*

### 시간표 관리
![시간표 관리](screenshots/timetable.png)
*수정 가능한 시간표 인터페이스 - 드래그 앤 드롭으로 쉽게 편집*

### 스터디 플래너
![스터디 플래너](screenshots/planner.png)
*개인 맞춤형 학습 계획 및 진도 관리*

### 커뮤니티
![커뮤니티](screenshots/community.png)
*학과별 소통 공간 및 자료 공유*

### 관리자 페이지
![관리자 페이지](screenshots/admin_page.png)
*Django 관리자 인터페이스*

## 기대 효과
- 분산된 정보의 통합 관리로 효율성 향상
- 개인 맞춤형 학습 분석
- 학업 및 프로젝트 관리의 투명성 증대
- 협업 및 소통 강화

## 배포

### EC2 배포 (교수님 예시 기반)

**1. Cursor/VSCode로 EC2 접속**
```bash
# SSH 설정
Host planit-ec2
    HostName 35.163.12.109
    User ubuntu
    IdentityFile /path/to/ec2-kafa-2-key.pem
```

**2. EC2에서 프로젝트 클론**
```bash
# 현재 폴더 확인
ll

# Git 저장소 클론
git clone https://github.com/whwjdgml0508/planit.git
cd planit

# Git 설정
git config user.name "ec2-planit"
git config user.email "ec2-planit@test.com"
```

**3. 간단 배포 실행**
```bash
chmod +x simple-deploy.sh
./simple-deploy.sh
```

**4. 접속 확인**
- http://planit.boramae.club
- http://35.163.12.109
- 관리자: http://planit.boramae.club/admin/

### 수동 배포
자세한 배포 가이드는 [DEPLOYMENT.md](DEPLOYMENT.md)를 참조하세요.

## 🚀 배포 정보

### 서버 환경
- **서버**: AWS EC2 (Ubuntu 22.04 LTS)
- **IP 주소**: 35.163.12.109
- **도메인**: planit.boramae.club
- **웹서버**: Nginx
- **WSGI 서버**: Gunicorn
- **데이터베이스**: MySQL

### 배포 아키텍처
```
Internet → Nginx (Port 80) → Gunicorn (Port 8000) → Django Application
                                                   ↓
                                              MySQL Database
```

### 주요 배포 파일
- `simple-deploy.sh` - 간단 배포 스크립트
- `deploy.sh` - 완전 자동화 배포 스크립트
- `nginx.conf` - Nginx 웹서버 설정
- `planit.service` - systemd 서비스 설정
- `gunicorn.conf.py` - Gunicorn WSGI 서버 설정

## 🎉 배포 완료!

**PlanIt이 성공적으로 배포되었습니다!**

### 🌐 접속 주소
- **메인 사이트**: http://planit.boramae.club
- **IP 직접 접속**: http://35.163.12.109
- **관리자 페이지**: http://planit.boramae.club/admin/

### 화면

### 📊 개발 현황

#### 서버 배포 및 운영
- [x] EC2 배포 설정 완료
- [x] **실제 EC2 배포 완료** ✅
- [x] **도메인 연결 완료** ✅
- [x] **Nginx 웹서버 설정** ✅
- [x] **MySQL 데이터베이스 연동** ✅
- [x] **Gunicorn 설정 완료** ✅
- [x] **정적 파일 수집 완료** ✅
- [x] **슈퍼유저 계정 생성** ✅
- [x] **서버 안정성 개선** ✅
- [x] **자동 배포 스크립트 구현** ✅

#### 크로스 플랫폼 앱 개발 🆕
- [x] **Android 앱 개발 환경 구축** ✅
- [x] **WebView 기반 Android 앱 구현** ✅
- [x] **Cordova 하이브리드 앱 설정** ✅
- [x] **Electron 데스크톱 앱 구현** ✅
- [x] **Windows EXE 빌드 시스템** ✅
- [x] **APK 자동 빌드 스크립트** ✅
- [x] **다양한 빌드 옵션 제공** ✅

#### 🎯 향후 개발 계획

## 🔧 트러블슈팅

### Server Error (500) 발생 시

**증상**: 특정 페이지 접속 시 "Server Error (500)" 발생

**원인**: templatetags 디렉토리의 파일들이 서버에 복사되지 않음

**해결 방법**:

1. **안전 배포 스크립트 사용** (권장):
```powershell
.\deploy_safe.ps1
```

2. **수동 복사**:
```powershell
# timetable templatetags 복사
scp -i ~/.ssh/ec2-kafa-2-key.pem -r timetable/templatetags/* ubuntu@35.163.12.109:/home/ubuntu/planit/timetable/templatetags/

# planner templatetags 복사
scp -i ~/.ssh/ec2-kafa-2-key.pem -r planner/templatetags/* ubuntu@35.163.12.109:/home/ubuntu/planit/planner/templatetags/

# 서버 재시작
ssh -i ~/.ssh/ec2-kafa-2-key.pem ubuntu@35.163.12.109 "sudo systemctl restart planit"
```

3. **서버 로그 확인**:
```bash
ssh -i ~/.ssh/ec2-kafa-2-key.pem ubuntu@35.163.12.109 "sudo journalctl -u planit -n 50"
```

### 주요 체크리스트
- [ ] templatetags 디렉토리에 `__init__.py` 파일 존재
- [ ] templatetags 디렉토리의 모든 `.py` 파일 복사됨
- [ ] 서버 재시작 후 정상 작동 확인
- [ ] 주요 페이지 HTTP 200 응답 확인

## 🚀 향후 개발 계획

- 콘텐츠 기능 강화: 파일 공유, 통합 검색
- 커뮤니티 기능: 오류 수정
- 프로필 설정
- HTTPS 적용 및 SSL 인증서 설정
- CI/CD 파이프라인 구축

## 라이선스
이 프로젝트는 교육 목적으로 개발되었습니다.
