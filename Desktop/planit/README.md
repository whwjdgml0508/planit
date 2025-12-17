# PlanIt - 생도 학습 관리 플랫폼

## 프로젝트 개요
학습 데이터를 통합하고 학과 커뮤니티를 연계하여 생도 생활의 효율성과 소통을 강화하는 **웹 기반 학습 관리 플랫폼**

## 주요 기능

### 1. 스터디 플래너 및 학습 진도 관리
- **시간표 관리**: 드래그 앤 드롭으로 쉬운 시간표 편집 및 커스터마이징
- **학습 플래너**: 일일 계획 수립 및 목표 설정
- **진도 추적**: 과목별 학습 진행률 시각화
- **과목 관리**: 평가 방식 및 세부 정보 기록

### 2. 커뮤니티 기능
- **학과별 소통**: 공지사항, 학습자료, 시험정보 등 카테고리별 게시판
- **자료 공유**: 다중 파일 업로드 및 드래그 앤 드롭 지원
- **사용자 편의성**: 댓글/답글 기능, 게시글 검색, 필터링

### 3. PWA (Progressive Web App) 지원 🆕
- **설치 없는 앱 사용**: 브라우저에서 "홈 화면에 추가"를 통해 앱처럼 사용 가능
- **반응형 디자인**: PC, 태블릿, 모바일 등 모든 기기에서 최적화된 화면 제공
- **접근성**: 별도의 스토어 다운로드 없이 URL 접속만으로 즉시 이용 가능

### 4. 통합 인증 시스템
- **유연한 로그인**: 학번(7자리) 또는 사용자 ID로 로그인 가능
- **보안**: 안전한 비밀번호 관리 및 세션 처리

## 기술 스택
- **Backend**: Django 4.2.25, Django REST Framework
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (개발용), MySQL (배포용)
- **Web Server**: Nginx
- **WSGI**: Gunicorn
- **Infrastructure**: AWS EC2 (Ubuntu 22.04)
- **Domain**: http://planit.boramae.club

## 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/whwjdgml0508/planit.git
cd planit
```

### 2. 가상환경 생성 및 활성화
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

### 5. 슈퍼유저 생성
```bash
python manage.py createsuperuser
```

### 6. 개발 서버 실행
```bash
python manage.py runserver
```
브라우저에서 `http://127.0.0.1:8000`으로 접속하여 확인할 수 있습니다.

## 프로젝트 구조
```
planit/
├── accounts/           # 사용자 인증, 프로필 관리
├── timetable/          # 시간표, 과목 관리
├── planner/            # 플래너, 할 일, 목표 관리
├── community/          # 게시판, 댓글, 자료실
├── templates/          # HTML 템플릿
├── static/             # 정적 파일 (CSS, JS, Images)
├── media/              # 사용자 업로드 파일
├── planit_project/     # Django 프로젝트 설정
├── deploy/             # 배포 관련 스크립트 및 설정
├── manage.py           # Django 관리 스크립트
├── requirements.txt    # 의존성 패키지 목록
└── README.md           # 프로젝트 문서
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

## 배포 정보

### 서버 환경
- **서버**: AWS EC2 (Ubuntu 22.04 LTS)
- **IP 주소**: 35.163.12.109
- **도메인**: planit.boramae.club
- **웹서버**: Nginx (Reverse Proxy)
- **WSGI**: Gunicorn

### 배포 아키텍처
```
Internet → Nginx (Port 80) → Gunicorn (Port 8000) → Django Application
                                                   ↓
                                              MySQL Database
```

### 주요 배포 스크립트
- `simple-deploy.sh`: 간단 배포 스크립트
- `deploy/auto_deploy.sh`: 자동 배포 스크립트

## 라이선스
이 프로젝트는 교육 목적으로 개발되었습니다.
