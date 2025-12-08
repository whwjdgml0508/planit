# 🔐 GitHub Secrets 설정 가이드

자동 배포를 위해 GitHub Repository에서 다음 Secrets를 설정해야 합니다.

## 📋 설정 방법

1. **GitHub 저장소로 이동**
   - https://github.com/whwjdgml0508/planit 접속

2. **Settings 탭 클릭**
   - 저장소 상단의 "Settings" 탭 클릭

3. **Secrets and variables 메뉴**
   - 왼쪽 사이드바에서 "Secrets and variables" > "Actions" 클릭

4. **New repository secret 버튼 클릭**

## 🔑 설정할 Secrets

### 1. HOST
- **Name**: `HOST`
- **Value**: `35.163.12.109`

### 2. USERNAME  
- **Name**: `USERNAME`
- **Value**: `ubuntu`

### 3. SSH_KEY
- **Name**: `SSH_KEY`
- **Value**: 아래 SSH 키 전체 내용 복사
```
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAvdw183F3wpo+Pg0udF1Cn0QstZMi3OSAG0Q6Zn6DZGXZxdXF
WEGAnpSpR6eD2ooySuydYFWan48IK9/YmX9XsITk5HwY94F7K95u7vyBTVmOIN08
Lopg6pn0EUlnwBCWSLnPuLRrlpNA8+GD8n8b6+gRcKiIh1jKXgVR3F0lLXgTSq9E
dkQOaX0Yxsumh0+DZE1HdtzeiPayGR4tF/jOdOEC+8wQ1W2RYBwvEi6XpcyRxIl4
T2F9Ty9M850+gGhiJCdRoEuILKQDPYAIT98lyYny0GftjUUHX4zJ4vikfqMamcxJ
Z8azHxOcuXHRoGD+9/gLkojhU5n8LJelpjcJaQIDAQABAoIBAQCRA8bth8hqijdq
W9UUqjr9vSvNEHI7eAhlSyq0KIOhRq4cjpgqPfXIqlHV2hw66v1Y/vuBnkD5CF28
bUBalcpbmFXgMu069tomesIOpiz48KM/dNvHzIgUCL1ECuZE7CZtrAb91Eis/RJK
dQC8Utv3xwyzGPcXMfl38OZCw55m6BIdqZSHBAgzoIWWYnom1V/9L+0tSxh6g9Ym
SBtTIusvMo0+WXdD7OGlq79r4TMGb2qZhHjhBwSJwlVK75fjS0KDLUkxLosOSCH+
FeqlSrmDysxEkO44gMVoNKY3UwTAIsHiuWDe9g5cgwkOr9Zd7oQZ72iWoHFcI0AS
Yo2Bytp1AoGBAPbN5piHzxlBLwBROHxeb3puGcr2JOrd4a57f5pPp2W7+S9uvLWR
AgsJfI+WJs5Owo+QG40+1nDdn4N5gwi6nRjWtpeHg2B1dQNYdKuZuuT0y8z+ehr4
WvwIUNxI1I3qdY4MpKj7SM4z7eh3E6eBKJ7nDkP4VGL7lG6jGkE7hMlfAoGBAMTv
KKIHAyK0uznIn6ALeJjCUssd4CfN21k0siB5dM13OcNqk520FQFjOQrg/G76xvd+
/lxd0uuWETilvLApEIHzLm9oNh0axAe7zd7pfbi1qt9DWZwjnr0VdzBgwj+mYbvh
bLs8U69xHwRaiwVJKDGgiXTtL/pQPrptDpQ3l/o3AoGAJys8Wp7LJmXq8LDzNwHB
zXtlyolQCJpYM9nTwYi8t2+it31qo6I04c2KoDsjQ4DKbgBf7wW3AMibhUEmo58C
Savh5KCUIB3kCTjjo0xNlgKnyYvlkxwxTGiBdMR2P2OjbnzhMRRYVKl3K3qieuYL
rVRcNjtWITNuNjTaeNnaVB8CgYAO8YrmyJtvTcGLP/ME5PnwtYYszYaN3qwPV9VQ
a4b2dF6YuoSbCegyI8JXVf0xuqvQaf2JKsFviQKjhsgLogITqk1SvNimWrqXT6Pu
j08v7fEaYfTxyS4pcPCLZjw3MjvmUtO6XXiILpBI90nnS8bWBTWI/tqOJvqrkMzz
aEiK/wKBgQDlCVMx+cE4p717SJ3V+agfEW6ifD5j4UziI79ajiCiHcENLnwzvKrD
+OdEHe0/qCpd0jWQB40UE7zO/jphxuBL5v3OEbnfxjkd3BXUXb1rxQ0xKEsb1jPu
DCAUPYseq+AKV7ycrzhUMrhAUP6PQgqdZVSSEQnkKXJk6NJedDI6KQ==
-----END RSA PRIVATE KEY-----
```

## ✅ 설정 완료 후

1. 모든 3개의 Secrets가 설정되었는지 확인
2. 코드를 main 브랜치에 푸시하면 자동 배포가 시작됩니다
3. Actions 탭에서 배포 진행 상황을 확인할 수 있습니다

## 🚀 자동 배포 동작 방식

- **트리거**: main 브랜치에 코드 푸시
- **제외 파일**: README.md, 스크린샷, 마크다운 파일
- **배포 과정**:
  1. 코드 검증 (Django check)
  2. 서버 접속
  3. 최신 코드 가져오기
  4. 의존성 업데이트
  5. 데이터베이스 마이그레이션
  6. 정적 파일 수집
  7. 서버 재시작
  8. 배포 완료 확인

## 📱 배포 상태 확인

- **GitHub Actions**: https://github.com/whwjdgml0508/planit/actions
- **웹사이트**: http://planit.boramae.club
- **배포 로그**: Actions 탭에서 실시간 확인 가능
