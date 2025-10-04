from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

User = get_user_model()

class Subject(models.Model):
    """과목 모델"""
    
    SUBJECT_TYPE_CHOICES = [
        ('MAJOR', '전공'),
        ('GENERAL', '교양'),
        ('MILITARY', '군사학'),
        ('PHYSICAL', '체육'),
        ('OTHER', '기타'),
    ]
    
    EVALUATION_TYPE_CHOICES = [
        ('EXAM', '시험'),
        ('REPORT', '보고서'),
        ('PRESENTATION', '발표'),
        ('PROJECT', '프로젝트'),
        ('PARTICIPATION', '참여도'),
        ('MIXED', '혼합'),
    ]
    
    # 기본 정보
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=100, verbose_name='과목명')
    code = models.CharField(max_length=20, blank=True, verbose_name='과목코드')
    professor = models.CharField(max_length=50, blank=True, verbose_name='교수명')
    credits = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)],
        default=3,
        verbose_name='학점'
    )
    
    # 분류
    subject_type = models.CharField(
        max_length=10,
        choices=SUBJECT_TYPE_CHOICES,
        default='MAJOR',
        verbose_name='과목 구분'
    )
    
    # 평가 방식
    evaluation_type = models.CharField(
        max_length=15,
        choices=EVALUATION_TYPE_CHOICES,
        default='EXAM',
        verbose_name='평가 방식'
    )
    
    # 추가 정보
    classroom = models.CharField(max_length=50, blank=True, verbose_name='강의실')
    note = models.TextField(max_length=500, blank=True, verbose_name='메모')
    color = models.CharField(
        max_length=7,
        default='#007bff',
        help_text='시간표에서 표시될 색상 (HEX 코드)',
        verbose_name='색상'
    )
    
    # 메타데이터
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '과목'
        verbose_name_plural = '과목들'
        ordering = ['name']
        
    def __str__(self):
        return f"{self.name} ({self.professor})"

class TimeSlot(models.Model):
    """시간표 슬롯 모델"""
    
    DAY_CHOICES = [
        ('MON', '월요일'),
        ('TUE', '화요일'),
        ('WED', '수요일'),
        ('THU', '목요일'),
        ('FRI', '금요일'),
        ('SAT', '토요일'),
        ('SUN', '일요일'),
    ]
    
    PERIOD_CHOICES = [
        (1, '1교시 (09:00-09:50)'),
        (2, '2교시 (10:00-10:50)'),
        (3, '3교시 (11:00-11:50)'),
        (4, '4교시 (12:00-12:50)'),
        (5, '5교시 (13:00-13:50)'),
        (6, '6교시 (14:00-14:50)'),
        (7, '7교시 (15:00-15:50)'),
        (8, '8교시 (16:00-16:50)'),
        (9, '9교시 (17:00-17:50)'),
        (10, '10교시 (18:00-18:50)'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='time_slots')
    day = models.CharField(max_length=3, choices=DAY_CHOICES, verbose_name='요일')
    period = models.IntegerField(
        choices=PERIOD_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='교시'
    )
    
    # 추가 정보
    location = models.CharField(max_length=50, blank=True, verbose_name='장소')
    note = models.CharField(max_length=200, blank=True, verbose_name='메모')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '시간표 슬롯'
        verbose_name_plural = '시간표 슬롯들'
        unique_together = ['subject', 'day', 'period']
        ordering = ['day', 'period']
        
    def __str__(self):
        return f"{self.subject.name} - {self.get_day_display()} {self.get_period_display()}"
    
    def get_time_range(self):
        """교시에 따른 시간 범위 반환"""
        time_ranges = {
            1: '09:00-09:50',
            2: '10:00-10:50',
            3: '11:00-11:50',
            4: '12:00-12:50',
            5: '13:00-13:50',
            6: '14:00-14:50',
            7: '15:00-15:50',
            8: '16:00-16:50',
            9: '17:00-17:50',
            10: '18:00-18:50',
        }
        return time_ranges.get(self.period, '')

class Semester(models.Model):
    """학기 모델"""
    
    SEMESTER_CHOICES = [
        ('SPRING', '1학기'),
        ('SUMMER', '여름학기'),
        ('FALL', '2학기'),
        ('WINTER', '겨울학기'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='semesters')
    year = models.IntegerField(verbose_name='년도')
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES, verbose_name='학기')
    is_current = models.BooleanField(default=False, verbose_name='현재 학기')
    
    start_date = models.DateField(verbose_name='시작일')
    end_date = models.DateField(verbose_name='종료일')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '학기'
        verbose_name_plural = '학기들'
        unique_together = ['user', 'year', 'semester']
        ordering = ['-year', '-semester']
        
    def __str__(self):
        return f"{self.year}년 {self.get_semester_display()}"
    
    def save(self, *args, **kwargs):
        # 현재 학기로 설정할 때 다른 학기들의 is_current를 False로 변경
        if self.is_current:
            Semester.objects.filter(user=self.user, is_current=True).update(is_current=False)
        super().save(*args, **kwargs)
