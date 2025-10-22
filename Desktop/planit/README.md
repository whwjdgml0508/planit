# PlanIt - 생도 학습 관리 플랫폼

## 프로젝트 개요
학습 데이터를 통합하고 학과 커뮤니티를 연계하여 생도 생활의 효율성과 소통을 강화하는 웹사이트

## 주요 기능

### 1. 스터디 플래너 및 학습 진도 관리
- 수정 가능한 시간표
- 각 과목별 평가 방식 기록
- 스터디 플래너 기능
- 학습 진도 추적

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

## 기술 스택
- **Backend**: Django 5.2.7
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (개발용), MySQL (배포용)
- **UI Framework**: Bootstrap 5 + Crispy Forms
- **웹서버**: Nginx
- **WSGI**: Gunicorn
- **배포**: AWS EC2 (Ubuntu 22.04)
- **도메인**: http://planit.boramae.club ✅ **배포 완료**

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
├── manage.py
├── requirements.txt
└── README.md
```

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

### 📊 개발 현황
- [x] 프로젝트 초기 설정
- [x] 사용자 인증 시스템 (accounts 앱)
- [x] 시간표 관리 기능 (timetable 앱)
- [x] 스터디 플래너 기능 (planner 앱)
- [x] 커뮤니티 기능 (community 앱)
- [x] 기본 UI/UX 구현 (Bootstrap 5)
- [x] EC2 배포 설정 완료
- [x] **실제 EC2 배포 완료** ✅
- [x] **도메인 연결 완료** ✅
- [x] **Nginx 웹서버 설정** ✅
- [x] **MySQL 데이터베이스 연동** ✅
- [x] **Gunicorn 설정 완료** ✅
- [x] **정적 파일 수집 완료** ✅
- [x] **슈퍼유저 계정 생성** ✅
- [ ] 로그인 500 오류 디버깅 및 해결
- [ ] Gunicorn 서비스 자동 시작 설정
- [ ] 통합 정보 관리 (E-class, 구글 클래스 연동)
- [ ] SSL 인증서 설정 (HTTPS)

## 라이선스
이 프로젝트는 교육 목적으로 개발되었습니다.
