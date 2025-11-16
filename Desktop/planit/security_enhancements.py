#!/usr/bin/env python3
"""
PlanIt 보안 강화 스크립트
입력 검증, CSRF 보호, SQL 인젝션 방지 등 보안 기능을 강화합니다.
"""

import os
import django
from pathlib import Path

def create_security_middleware():
    """보안 미들웨어 생성"""
    middleware_content = """
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
import re
import logging

logger = logging.getLogger(__name__)

class SecurityMiddleware(MiddlewareMixin):
    \"\"\"PlanIt 보안 미들웨어\"\"\"
    
    # 위험한 패턴들
    DANGEROUS_PATTERNS = [
        r'<script[^>]*>.*?</script>',  # XSS
        r'javascript:',               # JavaScript 프로토콜
        r'on\w+\s*=',                # 이벤트 핸들러
        r'union\s+select',           # SQL Injection
        r'drop\s+table',             # SQL Injection
        r'delete\s+from',            # SQL Injection
    ]
    
    def process_request(self, request):
        \"\"\"요청 처리 전 보안 검사\"\"\"
        
        # 1. SQL Injection 패턴 검사
        if self._check_sql_injection(request):
            logger.warning(f"SQL Injection 시도 감지: {request.META.get('REMOTE_ADDR')}")
            return HttpResponseForbidden("잘못된 요청입니다.")
        
        # 2. XSS 패턴 검사
        if self._check_xss_patterns(request):
            logger.warning(f"XSS 시도 감지: {request.META.get('REMOTE_ADDR')}")
            return HttpResponseForbidden("잘못된 요청입니다.")
        
        # 3. 파일 업로드 검사
        if request.FILES and not self._check_file_upload(request):
            logger.warning(f"위험한 파일 업로드 시도: {request.META.get('REMOTE_ADDR')}")
            return HttpResponseForbidden("허용되지 않는 파일 형식입니다.")
        
        return None
    
    def _check_sql_injection(self, request):
        \"\"\"SQL Injection 패턴 검사\"\"\"
        dangerous_sql = [
            'union select', 'drop table', 'delete from', 'insert into',
            'update set', 'alter table', 'create table', 'exec(',
            'execute(', 'sp_', 'xp_'
        ]
        
        # GET 파라미터 검사
        for key, value in request.GET.items():
            if any(pattern in value.lower() for pattern in dangerous_sql):
                return True
        
        # POST 데이터 검사
        if hasattr(request, 'POST'):
            for key, value in request.POST.items():
                if isinstance(value, str) and any(pattern in value.lower() for pattern in dangerous_sql):
                    return True
        
        return False
    
    def _check_xss_patterns(self, request):
        \"\"\"XSS 패턴 검사\"\"\"
        for pattern in self.DANGEROUS_PATTERNS:
            # GET 파라미터 검사
            for key, value in request.GET.items():
                if re.search(pattern, value, re.IGNORECASE):
                    return True
            
            # POST 데이터 검사
            if hasattr(request, 'POST'):
                for key, value in request.POST.items():
                    if isinstance(value, str) and re.search(pattern, value, re.IGNORECASE):
                        return True
        
        return False
    
    def _check_file_upload(self, request):
        \"\"\"파일 업로드 보안 검사\"\"\"
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.doc', '.docx']
        max_file_size = 10 * 1024 * 1024  # 10MB
        
        for file_field in request.FILES.values():
            # 파일 크기 검사
            if file_field.size > max_file_size:
                return False
            
            # 파일 확장자 검사
            file_ext = os.path.splitext(file_field.name)[1].lower()
            if file_ext not in allowed_extensions:
                return False
            
            # 파일 내용 검사 (간단한 매직 넘버 체크)
            file_field.seek(0)
            header = file_field.read(10)
            file_field.seek(0)
            
            # 실행 파일 헤더 검사
            if header.startswith(b'MZ') or header.startswith(b'\\x7fELF'):
                return False
        
        return True

class RateLimitMiddleware(MiddlewareMixin):
    \"\"\"요청 제한 미들웨어\"\"\"
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = {}  # IP별 요청 카운트
        super().__init__(get_response)
    
    def process_request(self, request):
        \"\"\"요청 제한 검사\"\"\"
        client_ip = self._get_client_ip(request)
        current_time = time.time()
        
        # 1분간 최대 100회 요청 제한
        if client_ip in self.requests:
            requests_in_minute = [req_time for req_time in self.requests[client_ip] 
                                if current_time - req_time < 60]
            
            if len(requests_in_minute) > 100:
                logger.warning(f"Rate limit 초과: {client_ip}")
                return HttpResponseForbidden("요청이 너무 많습니다. 잠시 후 다시 시도해주세요.")
            
            self.requests[client_ip] = requests_in_minute + [current_time]
        else:
            self.requests[client_ip] = [current_time]
        
        return None
    
    def _get_client_ip(self, request):
        \"\"\"클라이언트 IP 주소 획득\"\"\"
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
"""
    
    middleware_file = Path("planit_project/middleware/security.py")
    middleware_file.parent.mkdir(parents=True, exist_ok=True)
    middleware_file.write_text(middleware_content, encoding='utf-8')
    
    # __init__.py 파일 생성
    init_file = middleware_file.parent / "__init__.py"
    init_file.write_text("", encoding='utf-8')
    
    print(f"✅ 보안 미들웨어 생성: {middleware_file}")

def create_input_validators():
    """입력 검증 유틸리티"""
    validator_content = """
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re
import bleach

class InputValidator:
    \"\"\"입력 데이터 검증 유틸리티\"\"\"
    
    @staticmethod
    def validate_username(username):
        \"\"\"사용자명 검증\"\"\"
        if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
            raise ValidationError(_('사용자명은 3-20자의 영문, 숫자, 언더스코어만 허용됩니다.'))
        
        # 예약어 검사
        reserved_words = ['admin', 'root', 'system', 'test', 'guest']
        if username.lower() in reserved_words:
            raise ValidationError(_('예약된 사용자명입니다.'))
    
    @staticmethod
    def validate_password(password):
        \"\"\"비밀번호 강도 검증\"\"\"
        if len(password) < 8:
            raise ValidationError(_('비밀번호는 최소 8자 이상이어야 합니다.'))
        
        if not re.search(r'[A-Z]', password):
            raise ValidationError(_('비밀번호에 대문자가 포함되어야 합니다.'))
        
        if not re.search(r'[a-z]', password):
            raise ValidationError(_('비밀번호에 소문자가 포함되어야 합니다.'))
        
        if not re.search(r'[0-9]', password):
            raise ValidationError(_('비밀번호에 숫자가 포함되어야 합니다.'))
        
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
            raise ValidationError(_('비밀번호에 특수문자가 포함되어야 합니다.'))
    
    @staticmethod
    def sanitize_html(content):
        \"\"\"HTML 내용 정화\"\"\"
        allowed_tags = ['p', 'br', 'strong', 'em', 'u', 'ol', 'ul', 'li', 'a']
        allowed_attributes = {'a': ['href', 'title']}
        
        return bleach.clean(content, tags=allowed_tags, attributes=allowed_attributes)
    
    @staticmethod
    def validate_email_domain(email):
        \"\"\"이메일 도메인 검증\"\"\"
        allowed_domains = ['gmail.com', 'naver.com', 'daum.net', 'hanmail.net']
        domain = email.split('@')[1] if '@' in email else ''
        
        if domain not in allowed_domains:
            raise ValidationError(_('허용되지 않는 이메일 도메인입니다.'))
    
    @staticmethod
    def validate_file_content(file):
        \"\"\"파일 내용 검증\"\"\"
        # 파일 시그니처 검사
        file_signatures = {
            b'\\xff\\xd8\\xff': 'jpg',
            b'\\x89PNG\\r\\n\\x1a\\n': 'png',
            b'GIF87a': 'gif',
            b'GIF89a': 'gif',
            b'%PDF': 'pdf'
        }
        
        file.seek(0)
        header = file.read(10)
        file.seek(0)
        
        for signature, file_type in file_signatures.items():
            if header.startswith(signature):
                return file_type
        
        raise ValidationError(_('지원되지 않는 파일 형식입니다.'))

# Django Form에서 사용할 커스텀 검증자들
def validate_safe_content(value):
    \"\"\"안전한 내용 검증\"\"\"
    dangerous_patterns = [
        r'<script', r'javascript:', r'on\w+\s*=', 
        r'eval\s*\(', r'document\.', r'window\.'
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, value, re.IGNORECASE):
            raise ValidationError(_('허용되지 않는 내용이 포함되어 있습니다.'))

def validate_no_sql_injection(value):
    \"\"\"SQL 인젝션 방지 검증\"\"\"
    sql_keywords = [
        'union', 'select', 'drop', 'delete', 'insert', 'update',
        'alter', 'create', 'exec', 'execute', 'sp_', 'xp_'
    ]
    
    value_lower = value.lower()
    for keyword in sql_keywords:
        if keyword in value_lower:
            raise ValidationError(_('허용되지 않는 키워드가 포함되어 있습니다.'))
"""
    
    validator_file = Path("planit_project/utils/validators.py")
    validator_file.parent.mkdir(parents=True, exist_ok=True)
    validator_file.write_text(validator_content, encoding='utf-8')
    
    # __init__.py 파일 생성
    init_file = validator_file.parent / "__init__.py"
    init_file.write_text("", encoding='utf-8')
    
    print(f"✅ 입력 검증 유틸리티 생성: {validator_file}")

def create_security_settings():
    """보안 설정 파일"""
    settings_content = """
# PlanIt 보안 설정

# 보안 미들웨어 추가
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'planit_project.middleware.security.SecurityMiddleware',  # 커스텀 보안 미들웨어
    'planit_project.middleware.security.RateLimitMiddleware',  # 요청 제한
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF 보호
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CSRF 보호 강화
CSRF_COOKIE_SECURE = True  # HTTPS에서만 CSRF 쿠키 전송
CSRF_COOKIE_HTTPONLY = True  # JavaScript에서 CSRF 쿠키 접근 차단
CSRF_COOKIE_SAMESITE = 'Strict'  # SameSite 정책
CSRF_USE_SESSIONS = True  # 세션 기반 CSRF 토큰

# 세션 보안
SESSION_COOKIE_SECURE = True  # HTTPS에서만 세션 쿠키 전송
SESSION_COOKIE_HTTPONLY = True  # JavaScript에서 세션 쿠키 접근 차단
SESSION_COOKIE_SAMESITE = 'Strict'  # SameSite 정책
SESSION_COOKIE_AGE = 3600  # 1시간 후 세션 만료
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # 브라우저 종료 시 세션 만료

# 보안 헤더
SECURE_BROWSER_XSS_FILTER = True  # XSS 필터 활성화
SECURE_CONTENT_TYPE_NOSNIFF = True  # MIME 타입 스니핑 방지
SECURE_HSTS_SECONDS = 31536000  # HSTS 1년
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # 서브도메인 포함
SECURE_HSTS_PRELOAD = True  # HSTS 프리로드
X_FRAME_OPTIONS = 'DENY'  # 프레임 삽입 방지

# SSL/TLS 설정
SECURE_SSL_REDIRECT = True  # HTTP를 HTTPS로 리다이렉트
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# 파일 업로드 보안
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
FILE_UPLOAD_PERMISSIONS = 0o644

# 로깅 설정
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'security.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'planit_project.middleware.security': {
            'handlers': ['security_file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}

# 비밀번호 검증
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'planit_project.utils.validators.CustomPasswordValidator',
    },
]

# 데이터베이스 보안
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'sql_mode': 'STRICT_TRANS_TABLES',  # 엄격한 SQL 모드
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# 허용된 호스트 (프로덕션에서 반드시 설정)
ALLOWED_HOSTS = ['planit.boramae.club', 'www.planit.boramae.club']

# 디버그 모드 (프로덕션에서 반드시 False)
DEBUG = False

# 관리자 정보
ADMINS = [
    ('PlanIt Admin', 'admin@planit.boramae.club'),
]

# 에러 리포팅
MANAGERS = ADMINS
"""
    
    settings_file = Path("planit_project/settings/security.py")
    settings_file.parent.mkdir(parents=True, exist_ok=True)
    settings_file.write_text(settings_content, encoding='utf-8')
    
    print(f"✅ 보안 설정 파일 생성: {settings_file}")

if __name__ == "__main__":
    print("🔒 PlanIt 보안 강화 도구")
    print("=" * 50)
    
    # 1. 보안 미들웨어 생성
    create_security_middleware()
    
    # 2. 입력 검증 유틸리티 생성
    create_input_validators()
    
    # 3. 보안 설정 파일 생성
    create_security_settings()
    
    print("\n🎉 보안 강화 파일 생성 완료!")
    print("📋 추가 작업:")
    print("  1. settings.py에 보안 설정 적용")
    print("  2. 미들웨어 등록")
    print("  3. 폼에 검증자 적용")
    print("  4. 보안 테스트 실행")
    print("  5. SSL 인증서 설정 확인")
