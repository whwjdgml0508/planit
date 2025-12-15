import os
import django
import sqlite3

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.development')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

print("=" * 60)
print("데이터베이스 상태 확인")
print("=" * 60)

# SQLite 데이터베이스 직접 확인
db_path = 'db.sqlite3'
if os.path.exists(db_path):
    file_size = os.path.getsize(db_path)
    modified_time = os.path.getmtime(db_path)
    from datetime import datetime
    mod_date = datetime.fromtimestamp(modified_time)
    
    print(f"\n데이터베이스 파일 정보:")
    print(f"  - 경로: {os.path.abspath(db_path)}")
    print(f"  - 크기: {file_size:,} bytes ({file_size/1024:.2f} KB)")
    print(f"  - 마지막 수정: {mod_date}")
    
    # SQLite로 직접 연결해서 삭제된 사용자 확인
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 전체 사용자 수 확인
    cursor.execute("SELECT COUNT(*) FROM accounts_user")
    total_users = cursor.fetchone()[0]
    print(f"\n총 사용자 수: {total_users}")
    
    # 모든 사용자 정보
    cursor.execute("""
        SELECT id, username, student_id, first_name, last_name, 
               email, is_active, date_joined 
        FROM accounts_user 
        ORDER BY date_joined DESC
    """)
    users = cursor.fetchall()
    
    print("\n등록된 사용자 목록:")
    for user in users:
        user_id, username, student_id, first_name, last_name, email, is_active, date_joined = user
        print(f"\n  ID: {user_id}")
        print(f"  - 사용자명: {username}")
        print(f"  - 학번: {student_id}")
        print(f"  - 이름: {last_name}{first_name}")
        print(f"  - 이메일: {email}")
        print(f"  - 활성: {is_active}")
        print(f"  - 가입일: {date_joined}")
    
    conn.close()
else:
    print("데이터베이스 파일을 찾을 수 없습니다!")

print("\n" + "=" * 60)
print("Django ORM으로 확인:")
print("=" * 60)

all_users = User.objects.all()
print(f"\nDjango ORM 사용자 수: {all_users.count()}")

for user in all_users:
    print(f"\n  {user.username} (학번: {user.student_id})")
    print(f"  - 이름: {user.get_full_name()}")
    print(f"  - 가입일: {user.date_joined}")

print("\n" + "=" * 60)
