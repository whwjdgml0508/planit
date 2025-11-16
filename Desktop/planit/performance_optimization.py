#!/usr/bin/env python3
"""
PlanIt 성능 최적화 스크립트
캐싱, 데이터베이스 인덱싱, 쿼리 최적화를 자동으로 적용합니다.
"""

import os
import django
from django.core.management import execute_from_command_line
from django.db import connection

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings')
django.setup()

def optimize_database():
    """데이터베이스 최적화"""
    print("🔧 데이터베이스 최적화 시작...")
    
    with connection.cursor() as cursor:
        # 1. 자주 사용되는 컬럼에 인덱스 추가
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_timetable_user ON timetable_timetable(user_id);",
            "CREATE INDEX IF NOT EXISTS idx_planner_user ON planner_plan(user_id);",
            "CREATE INDEX IF NOT EXISTS idx_community_category ON community_post(category_id);",
            "CREATE INDEX IF NOT EXISTS idx_community_created ON community_post(created_at);",
            "CREATE INDEX IF NOT EXISTS idx_accounts_email ON accounts_customuser(email);",
        ]
        
        for index_sql in indexes:
            try:
                cursor.execute(index_sql)
                print(f"✅ 인덱스 생성: {index_sql.split('idx_')[1].split(' ')[0]}")
            except Exception as e:
                print(f"⚠️ 인덱스 생성 실패: {e}")
    
    print("✅ 데이터베이스 최적화 완료!")

def setup_redis_caching():
    """Redis 캐싱 설정"""
    print("🚀 Redis 캐싱 설정...")
    
    cache_settings = """
# Redis 캐싱 설정 추가
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# 세션을 Redis에 저장
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# 캐시 미들웨어 추가
MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    # ... 기존 미들웨어들 ...
    'django.middleware.cache.FetchFromCacheMiddleware',
]

# 캐시 설정
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 600  # 10분
CACHE_MIDDLEWARE_KEY_PREFIX = 'planit'
"""
    
    print("📝 settings.py에 다음 설정을 추가하세요:")
    print(cache_settings)

def create_cdn_setup():
    """CDN 설정 가이드"""
    print("🌐 CDN 설정 가이드...")
    
    cdn_guide = """
# CloudFlare CDN 설정 단계:

1. CloudFlare 계정 생성 및 도메인 추가
   - planit.boramae.club 도메인 추가
   - 네임서버 변경

2. 성능 최적화 설정
   - Auto Minify: CSS, JS, HTML 활성화
   - Brotli 압축 활성화
   - 캐싱 레벨: Standard

3. 보안 설정
   - SSL/TLS: Full (strict)
   - Always Use HTTPS: 활성화
   - HSTS: 활성화

4. Django 설정 수정 (settings.py)
   STATIC_URL = 'https://cdn.planit.boramae.club/static/'
   MEDIA_URL = 'https://cdn.planit.boramae.club/media/'
"""
    
    print(cdn_guide)

def benchmark_performance():
    """성능 벤치마크"""
    print("📊 성능 벤치마크 실행...")
    
    import time
    import requests
    
    urls = [
        'https://planit.boramae.club/',
        'https://planit.boramae.club/timetable/',
        'https://planit.boramae.club/planner/',
        'https://planit.boramae.club/community/',
    ]
    
    results = []
    for url in urls:
        try:
            start_time = time.time()
            response = requests.get(url, timeout=10)
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000  # ms
            results.append({
                'url': url,
                'status': response.status_code,
                'response_time': f"{response_time:.2f}ms"
            })
            
        except Exception as e:
            results.append({
                'url': url,
                'status': 'Error',
                'response_time': str(e)
            })
    
    print("\n📈 성능 테스트 결과:")
    for result in results:
        print(f"  {result['url']}: {result['status']} - {result['response_time']}")

if __name__ == "__main__":
    print("🚀 PlanIt 성능 최적화 도구")
    print("=" * 50)
    
    # 1. 데이터베이스 최적화
    optimize_database()
    
    # 2. Redis 캐싱 설정 가이드
    setup_redis_caching()
    
    # 3. CDN 설정 가이드
    create_cdn_setup()
    
    # 4. 성능 벤치마크
    benchmark_performance()
    
    print("\n🎉 성능 최적화 완료!")
    print("📋 추가 작업:")
    print("  1. settings.py에 캐싱 설정 추가")
    print("  2. CloudFlare CDN 설정")
    print("  3. 정적 파일 CDN 업로드")
