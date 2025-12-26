#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.production')
django.setup()

from django.db import connection

cursor = connection.cursor()
try:
    cursor.execute("ALTER TABLE timetable_timeslot ADD COLUMN semester_id char(32) NULL")
    print("semester_id 컬럼이 추가되었습니다.")
except Exception as e:
    print(f"오류 또는 이미 존재: {e}")

connection.close()
