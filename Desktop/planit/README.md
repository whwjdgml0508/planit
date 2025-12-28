# 🎯 PlanIt - 생도 학습 관리 플랫폼

<div align="center">

![PlanIt Logo](https://img.shields.io/badge/PlanIt-학습관리플랫폼-blue?style=for-the-badge)
[![Django](https://img.shields.io/badge/Django-4.2.25-green?style=flat-square&logo=django)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?style=flat-square&logo=bootstrap)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-Educational-yellow?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-success?style=flat-square)](http://planit.boramae.club)

**학습 데이터 통합 · 학과 커뮤니티 연계 · 생도 생활 효율화**

[🌐 Live Demo](http://planit.boramae.club) · [📖 Documentation](DEPLOYMENT.md) · [🐛 Report Bug](https://github.com/whwjdgml0508/planit/issues)

</div>

---

## 📋 목차

- [프로젝트 소개](#-프로젝트-소개)
- [주요 기능](#-주요-기능)
- [기술 스택](#-기술-스택)
- [시작하기](#-시작하기)
- [프로젝트 구조](#-프로젝트-구조)
- [배포 정보](#-배포-정보)
- [개발 로드맵](#-개발-로드맵)
- [기여하기](#-기여하기)
- [라이선스](#-라이선스)

---

## 🎓 프로젝트 소개

**PlanIt**은 생도들의 학습 관리와 학과 커뮤니티를 하나로 통합한 웹 기반 플랫폼입니다. 

### 🎯 프로젝트 목표

- **학습 효율성 향상**: 시간표, 플래너, 진도 관리를 한 곳에서
- **소통 강화**: 커뮤니티를 통한 정보 공유 및 협업
- **접근성 개선**: 웹 기반으로 모든 기기에서 접근 가능
- **데이터 통합**: 학습 데이터를 체계적으로 관리하고 시각화

### 🌟 특징

- ✅ **올인원 플랫폼**: 시간표, 플래너, 커뮤니티 통합 관리
- ✅ **반응형 디자인**: PC, 태블릿, 모바일 완벽 지원
- ✅ **실시간 동기화**: 모든 기기에서 데이터 자동 동기화
- ✅ **보안**: CSRF 보호, 세션 관리, 안전한 파일 업로드

---

## 🚀 주요 기능

### 1️⃣ 시간표 & 학기 관리

#### 📅 시간표 관리
- **학기별 시간표**: 학기 단위로 시간표를 분리하여 관리
- **8교시 지원**: 1교시(08:10)부터 8교시(17:00)까지 완벽 지원
- **과목 커스터마이징**: 색상, 교수님, 강의실, 평가방식 설정
- **자동 학점 계산**: 학기별 총 학점 자동 집계
- **학기 진행률**: 시작일~종료일 기준 학기 진행률 표시

#### 📚 과목 자료 관리
- **강의계획서 업로드**: 과목별 강의계획서 저장
- **수업자료 관리**: 강의자료, 과제, 시험자료 등 분류별 관리
- **파일 형식 지원**: PDF, DOC, PPT, 이미지 등 다양한 형식

#### 🗓️ 학기 관리
- **다중 학기 지원**: 1학기, 2학기, 동계학기 관리
- **현재 학기 설정**: 학기 별로 시간표 생성 가능
- **과목 수/학점 통계**: 학기별 과목 수 및 총 학점 표시

### 2️⃣ 스터디 플래너 & 학습 관리

#### 📝 일일 플래너
- **10분 단위 타임블록**: 세밀한 시간 관리 (학습/휴식/식사/운동)
- **할 일 관리**: 과목별 할 일 추가 및 우선순위 설정
- **일일 목표**: 오늘의 학습 목표 및 목표 학습시간 설정
- **진행률 시각화**: 할 일 완료율 실시간 표시

#### 🎯 목표 관리
- **다양한 목표 유형**: 일일/주간/월간/학기/사용자정의 목표
- **하위 목표**: 큰 목표를 작은 단위로 분할하여 체크리스트 관리
- **자동 진행률 계산**: 하위 목표 완료에 따른 자동 진행률 업데이트
- **달성 현황**: 목표 달성 여부 및 달성일시 기록

#### 📊 과제 관리
- **카테고리 분류**: 과제/시험/프로젝트/학습/개인/기타
- **우선순위 설정**: 낮음/보통/높음/긴급 4단계
- **마감일 관리**: D-Day 및 지연 일수 표시
- **진행률 추적**: 0-100% 진행률 관리

### 3️⃣ 커뮤니티 기능

#### 💬 소통 공간
- **5개 카테고리**: 공지사항, 학습자료, 시험정보, 체력평가, 자유게시판
- **게시글 유형**: 일반/질문/공지/팁 게시글 구분
- **태그 시스템**: 게시글에 태그 추가하여 분류
- **상단 고정**: 중요 게시글 상단 고정 기능

#### 📎 자료 공유
- **다중 파일 업로드**: 최대 5개 파일 동시 업로드
- **드래그 앤 드롭**: 파일을 끌어다 놓기만 하면 업로드
- **지원 형식**: 이미지(jpg, png, gif), 문서(pdf, doc, ppt, txt), 압축(zip)
- **다운로드 카운터**: 파일별 다운로드 횟수 추적
- **파일 크기 표시**: 자동 단위 변환 (B/KB/MB/GB)

#### 👥 사용자 상호작용
- **계층형 댓글**: 댓글과 대댓글(답글) 지원
- **좋아요 시스템**: 게시글 좋아요 및 좋아요 수 표시
- **북마크 기능**: 나중에 볼 게시글 저장
- **조회수 추적**: 게시글별 조회수 자동 증가
- **신고 기능**: 부적절한 게시글/댓글 신고 (스팸, 부적절, 괴롭힘, 저작권 등)

### 4️⃣ 사용자 & 인증 시스템

#### 👤 프로필 시스템
- **9개 학과 지원**: 국제관계학과, 국방경영학과, 항공우주정책학과, 컴퓨터과학과, 항공공학과, 우주공학과, 기계공학과, 전자통신공학과, 시스템공학과
- **4학년제 지원**: 1~4학년 학년 정보 관리
- **프로필 이미지**: 사용자 프로필 사진 업로드
- **자기소개**: 500자 이내 자기소개 작성
- **주간 학습 목표**: 개인별 주간 학습 목표 시간 설정

#### 🔐 유연한 로그인
- **이중 인증 방식**: 학번(7자리) 또는 사용자 ID로 로그인
- **커스텀 백엔드**: `StudentIdBackend`로 유연한 인증 처리
- **세션 관리**: 안전한 세션 유지 및 자동 로그아웃

#### 🛡️ 보안 기능
- **비밀번호 암호화**: Django의 PBKDF2 알고리즘 사용
- **CSRF 보호**: 모든 POST 요청에 토큰 검증
- **XSS 방지**: 사용자 입력 자동 이스케이핑
- **파일 검증**: 업로드 파일 형식 및 크기 제한

---

## 🛠️ 기술 스택

### Backend
- **Framework**: Django 4.2.25
- **API**: Django REST Framework 3.14.0
- **Authentication**: Django Auth + Custom Backend
- **Database ORM**: Django ORM

### Frontend
- **HTML5/CSS3**: 시맨틱 마크업 및 모던 CSS
- **JavaScript**: ES6+ 문법, Fetch API
- **UI Framework**: Bootstrap 5
- **Icons**: Font Awesome 6
- **Forms**: Django Crispy Forms + Bootstrap 5

### Database
- **Development**: SQLite 3
- **Production**: MySQL 8.0
- **Caching**: Redis 5.0.1 (선택적)

### DevOps & Infrastructure
- **Web Server**: Nginx 1.18
- **WSGI Server**: Gunicorn 23.0.0
- **Cloud**: AWS EC2 (Ubuntu 22.04 LTS)
- **Domain**: planit.boramae.club
- **Static Files**: WhiteNoise 6.7.0

### Additional Tools
- **Image Processing**: Pillow 10.4.0
- **Environment**: python-decouple 3.8
- **CORS**: django-cors-headers 4.3.1
- **JWT**: djangorestframework-simplejwt 5.3.0
- **API Docs**: drf-spectacular 0.27.0
- **Filtering**: django-filter 23.5

---

## 🏁 시작하기

### 📋 사전 요구사항

- Python 3.11 이상
- pip (Python 패키지 관리자)
- Git
- (선택) MySQL 8.0 (프로덕션 환경)

### 🔧 설치 방법

#### 1. 저장소 클론
```bash
git clone https://github.com/whwjdgml0508/planit.git
cd planit
```

#### 2. 가상환경 생성 및 활성화
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. 의존성 패키지 설치
```bash
pip install -r requirements.txt
```

#### 4. 환경 변수 설정
```bash
# .env.example을 .env로 복사
cp .env.example .env

# .env 파일 편집 (SECRET_KEY, DATABASE 설정 등)
```

#### 5. 데이터베이스 마이그레이션
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 6. 슈퍼유저 생성
```bash
python manage.py createsuperuser
```

#### 7. 정적 파일 수집
```bash
python manage.py collectstatic --noinput
```

#### 8. 개발 서버 실행
```bash
python manage.py runserver
```

브라우저에서 `http://127.0.0.1:8000` 접속

### 🐳 Docker로 실행 (선택)

```bash
# 개발 환경
docker-compose up -d

# 프로덕션 환경
docker-compose -f docker-compose.prod.yml up -d
```

---

## 📁 프로젝트 구조

```
planit/
├── 📂 accounts/              # 사용자 인증 및 프로필 관리
│   ├── models.py            # User 모델 (9개 학과, 프로필 이미지)
│   ├── views.py             # 로그인, 회원가입, 프로필
│   ├── forms.py             # 인증 폼
│   ├── backends.py          # StudentIdBackend (학번/ID 이중 인증)
│   └── urls.py              # 인증 관련 URL
│
├── 📂 timetable/             # 시간표 및 과목 관리
│   ├── models.py            # Subject, TimeSlot, Semester, SubjectFile 모델
│   ├── views.py             # 시간표/학기/과목 CRUD
│   └── templates/           # 시간표 템플릿 (14개)
│
├── 📂 planner/               # 플래너 및 학습 관리
│   ├── models.py            # Task, Goal, SubGoal, DailyPlanner, TimeBlock, TodoItem, StudySession 모델
│   ├── views.py             # 플래너/목표/과제 뷰
│   └── templates/           # 플래너 템플릿 (14개)
│
├── 📂 community/             # 커뮤니티 게시판
│   ├── models.py            # Category, Post, Comment, Attachment, Report 모델
│   ├── views.py             # 게시판 CRUD, 댓글, 좋아요, 북마크
│   ├── forms.py             # 게시글 작성 폼
│   └── templates/           # 커뮤니티 템플릿 (12개)
│
├── 📂 api/                   # REST API (선택적)
│   ├── serializers.py       # DRF Serializers
│   ├── views.py             # API ViewSets
│   └── urls.py              # API 엔드포인트
│
├── 📂 planit_project/        # Django 프로젝트 설정
│   ├── settings/            # 환경별 설정 분리
│   │   ├── base.py         # 공통 설정
│   │   ├── development.py  # 개발 환경
│   │   └── production.py   # 프로덕션 환경
│   ├── urls.py              # 메인 URL 라우팅
│   └── wsgi.py              # WSGI 설정
│
├── 📂 templates/             # HTML 템플릿 (40개+)
│   ├── base.html            # 베이스 템플릿 (네비게이션, 푸터)
│   ├── home.html            # 메인 페이지
│   ├── accounts/            # 로그인, 회원가입, 프로필 (4개)
│   ├── timetable/           # 시간표, 학기, 과목 (14개)
│   ├── planner/             # 플래너, 목표, 과제 (14개)
│   └── community/           # 게시판, 댓글 (12개)
│
├── 📂 static/                # 정적 파일
│   ├── css/                 # 스타일시트
│   ├── js/                  # JavaScript
│   ├── images/              # 이미지
│   └── icons/               # 파비콘 및 아이콘
│
├── 📂 media/                 # 사용자 업로드 파일
│   ├── profiles/            # 프로필 사진
│   ├── subject_files/       # 과목 자료 (강의계획서 등)
│   └── community/           # 게시글 첨부파일
│
├── 📂 deploy/                # 배포 스크립트
│   ├── auto_deploy.sh       # 자동 배포
│   └── nginx.conf           # Nginx 설정
│
├── 📂 screenshots/           # 스크린샷
│
├── 📄 manage.py              # Django 관리 스크립트
├── 📄 requirements.txt       # Python 의존성
├── 📄 Dockerfile             # Docker 이미지 빌드
├── 📄 docker-compose.yml     # Docker Compose 설정
├── 📄 gunicorn.conf.py       # Gunicorn 설정
├── 📄 nginx.conf             # Nginx 설정
├── 📄 .env.example           # 환경 변수 예시
├── 📄 .gitignore             # Git 제외 파일
├── 📄 README.md              # 프로젝트 문서
└── 📄 DEPLOYMENT.md          # 배포 가이드
```

---

## 🌐 배포 정보

### 🖥️ 서버 환경

| 항목 | 내용 |
|------|------|
| **클라우드** | AWS EC2 |
| **OS** | Ubuntu 22.04 LTS |
| **IP** | 35.163.12.109 |
| **도메인** | planit.boramae.club |
| **웹서버** | Nginx 1.18 |
| **WSGI** | Gunicorn 23.0.0 |
| **데이터베이스** | MySQL 8.0 |
| **Python** | 3.11+ |

### 🏗️ 배포 아키텍처

```
┌─────────────┐
│   Internet  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│  Nginx (Reverse Proxy)          │
│  - Port 80 (HTTP)                │
│  - Static Files Serving          │
│  - SSL Termination (예정)        │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│  Gunicorn (WSGI Server)         │
│  - Port 8000                     │
│  - 3 Worker Processes            │
│  - Unix Socket                   │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│  Django Application             │
│  - Business Logic                │
│  - Template Rendering            │
│  - Authentication                │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│  MySQL Database                 │
│  - User Data                     │
│  - Posts & Comments              │
│  - Timetables & Planners         │
└─────────────────────────────────┘
```

### 🚀 배포 스크립트

#### 간단 배포
```bash
# 로컬에서 실행
./simple-deploy.sh
```

#### 자동 배포
```bash
# 서버에서 실행
cd /home/ubuntu/planit
./deploy/auto_deploy.sh
```

#### 수동 배포
```bash
# 1. 코드 업데이트
git pull origin main

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 마이그레이션
python manage.py migrate

# 4. 정적 파일 수집
python manage.py collectstatic --noinput

# 5. 서비스 재시작
sudo systemctl restart planit
sudo systemctl restart nginx
```

### 📊 서비스 상태 확인

```bash
# PlanIt 서비스 상태
sudo systemctl status planit

# Nginx 상태
sudo systemctl status nginx

# 로그 확인
sudo journalctl -u planit -f
sudo tail -f /var/log/nginx/error.log
```

---

## 🗺️ 개발 로드맵

### ✅ 완료된 기능 (v1.0)
- [x] 사용자 인증 시스템 (학번/ID 이중 로그인)
- [x] 시간표 관리 (학기별 CRUD, 8교시 지원)
- [x] 학기 관리 (1학기/2학기/동계학기, 진행률)
- [x] 과목 자료 관리 (강의계획서, 수업자료 등)
- [x] 일일 플래너 (10분 단위 타임블록)
- [x] 목표 관리 (일일/주간/월간/학기 목표)
- [x] 하위 목표 체크리스트
- [x] 과제 관리 (우선순위, 마감일, 진행률)
- [x] 학습 세션 기록
- [x] 커뮤니티 게시판 (9개 카테고리)
- [x] 계층형 댓글/답글 시스템
- [x] 좋아요/북마크 기능
- [x] 다중 파일 업로드 (드래그 앤 드롭)
- [x] 게시글 신고 기능
- [x] 프로필 관리 (프로필 사진, 자기소개)
- [x] 9개 학과 지원
- [x] 반응형 디자인 (모바일/태블릿/데스크톱)
- [x] AWS EC2 Production 배포

### 🚧 진행 중 (v1.1)
- [ ] HTTPS 적용 (SSL 인증서)
- [ ] 성능 최적화 (캐싱, 쿼리 최적화)
- [ ] 모니터링 시스템 (로그, 메트릭)

### 📅 계획 중 (v2.0)
- [ ] 실시간 알림 (WebSocket)
- [ ] AI 학습 추천 시스템
- [ ] 그룹 스터디 기능
- [ ] 캘린더 통합 (Google Calendar)
- [ ] 다크 모드 지원
- [ ] 다국어 지원 (i18n)

---

## 🤝 기여하기

PlanIt 프로젝트에 기여해주셔서 감사합니다!

### 기여 방법

1. **Fork** 이 저장소
2. **Feature 브랜치** 생성 (`git checkout -b feature/AmazingFeature`)
3. **변경사항 커밋** (`git commit -m 'Add some AmazingFeature'`)
4. **브랜치에 Push** (`git push origin feature/AmazingFeature`)
5. **Pull Request** 생성

### 코드 스타일

- Python: PEP 8 가이드라인 준수
- JavaScript: ES6+ 문법 사용
- HTML/CSS: 시맨틱 마크업 및 BEM 방법론

### 이슈 리포트

버그를 발견하셨나요? [이슈를 등록](https://github.com/whwjdgml0508/planit/issues)해주세요.

---

## 📄 라이선스

이 프로젝트는 **교육 목적**으로 개발되었습니다.

---

## 👥 팀원

- **개발자**: [whwjdgml0508](https://github.com/whwjdgml0508)

---

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 다음으로 연락주세요:

- **GitHub Issues**: [프로젝트 이슈](https://github.com/whwjdgml0508/planit/issues)
- **Website**: [http://planit.boramae.club](http://planit.boramae.club)

---

<div align="center">

**Made with ❤️ by PlanIt Team**

⭐ 이 프로젝트가 도움이 되셨다면 Star를 눌러주세요!

</div>
