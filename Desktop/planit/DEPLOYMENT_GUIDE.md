# PlanIt 배포 가이드

## 🚀 안전한 배포 방법

### 1. 데이터 보존 배포 (권장)
```bash
ssh -i ec2-kafa-2-key.pem ubuntu@35.163.12.109
cd /home/ubuntu/planit
chmod +x deploy/safe_deploy.sh
./deploy/safe_deploy.sh
```

### 2. 데이터 복구 (과목이 사라졌을 때)
```bash
ssh -i ec2-kafa-2-key.pem ubuntu@35.163.12.109
cd /home/ubuntu/planit
chmod +x deploy/restore_data.sh
./deploy/restore_data.sh
```

### 3. 배포 후 확인
```bash
# 서버 상태 확인
ps aux | grep python

# 로그 확인
tail -f /home/ubuntu/planit/server.log

# 웹사이트 접속
# http://planit.boramae.club
```

## 🔍 문제 해결

### 과목이 사라졌을 때
```bash
# 1. 데이터 복구 스크립트 실행
./deploy/restore_data.sh

# 2. 수동으로 김공군 계정 확인
python manage.py shell -c "
from django.contrib.auth import get_user_model
from timetable.models import Subject
User = get_user_model()

try:
    kim_user = User.objects.get(username='김공군')
    subjects = Subject.objects.filter(user=kim_user)
    print(f'김공군 계정의 과목 수: {subjects.count()}개')
    for subject in subjects:
        print(f'- {subject.name}: {subject.color}')
except:
    print('김공군 계정을 찾을 수 없습니다.')
"
```

### 서버가 안 켜질 때
```bash
# 1. 프로세스 종료
pkill -f python
pkill -f gunicorn

# 2. 서버 재시작
cd /home/ubuntu/planit
source /home/ubuntu/planit/planit/venv/bin/activate
nohup python manage.py runserver 127.0.0.1:8000 > server.log 2>&1 &

# 3. 상태 확인
ps aux | grep python
```

## 📋 배포 전 체크리스트

- [ ] 로컬에서 테스트 완료
- [ ] Git에 커밋 및 푸시 완료
- [ ] 데이터베이스 백업 필요 여부 확인
- [ ] 안전 배포 스크립트 사용
- [ ] 배포 후 웹사이트 동작 확인
- [ ] 김공군 계정 과목 확인

## 🛡️ 데이터 보존 원리

1. **git stash**: 현재 변경사항(DB 포함) 임시 저장
2. **git pull**: 최신 코드만 가져오기
3. **migrate**: 데이터베이스 구조만 업데이트
4. **백업**: 배포 전 자동 백업 생성

이렇게 하면 기존 데이터가 보존됩니다!
