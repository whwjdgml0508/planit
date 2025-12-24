from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

User = get_user_model()

class Task(models.Model):
    """과제/할일 모델"""
    
    PRIORITY_CHOICES = [
        ('LOW', '낮음'),
        ('MEDIUM', '보통'),
        ('HIGH', '높음'),
        ('URGENT', '긴급'),
    ]
    
    STATUS_CHOICES = [
        ('TODO', '할 일'),
        ('IN_PROGRESS', '진행 중'),
        ('COMPLETED', '완료'),
        ('CANCELLED', '취소'),
    ]
    
    CATEGORY_CHOICES = [
        ('ASSIGNMENT', '과제'),
        ('EXAM', '시험'),
        ('PROJECT', '프로젝트'),
        ('STUDY', '학습'),
        ('PERSONAL', '개인'),
        ('OTHER', '기타'),
    ]
    
    # 기본 정보
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200, verbose_name='제목')
    description = models.TextField(blank=True, verbose_name='설명')
    
    # 분류 및 우선순위
    category = models.CharField(
        max_length=15,
        choices=CATEGORY_CHOICES,
        default='ASSIGNMENT',
        verbose_name='카테고리'
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='MEDIUM',
        verbose_name='우선순위'
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='TODO',
        verbose_name='상태'
    )
    
    # 시간 관련
    due_date = models.DateTimeField(null=True, blank=True, verbose_name='마감일')
    estimated_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.1), MaxValueValidator(999.99)],
        verbose_name='예상 소요시간(시간)'
    )
    actual_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.1), MaxValueValidator(999.99)],
        verbose_name='실제 소요시간(시간)'
    )
    
    # 연관 정보
    subject = models.ForeignKey(
        'timetable.Subject',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks',
        verbose_name='관련 과목'
    )
    
    # 완료 정보
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='완료일시')
    progress = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='진행률(%)'
    )
    
    # 메타데이터
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '과제/할일'
        verbose_name_plural = '과제/할일들'
        ordering = ['-priority', 'due_date', '-created_at']
        
    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
    
    def save(self, *args, **kwargs):
        # 진행률이 100%가 되면 자동으로 완료 상태로 변경
        if self.progress >= 100 and self.status != 'COMPLETED':
            self.status = 'COMPLETED'
            self.completed_at = timezone.now()
        # 완료 상태로 변경될 때 완료일시 설정
        elif self.status == 'COMPLETED' and not self.completed_at:
            self.completed_at = timezone.now()
            self.progress = 100
        # 완료 상태가 아니면 완료일시 초기화
        elif self.status != 'COMPLETED':
            self.completed_at = None
            
        super().save(*args, **kwargs)
    
    def is_overdue(self):
        """마감일이 지났는지 확인"""
        if self.due_date and self.status != 'COMPLETED':
            return timezone.now() > self.due_date
        return False
    
    def is_completed(self):
        """완료 상태인지 확인"""
        return self.status == 'COMPLETED'
    
    def days_overdue(self):
        """마감일로부터 며칠 지났는지 계산"""
        if self.is_overdue():
            delta = timezone.now() - self.due_date
            return delta.days
        return 0
    
    def get_priority_class(self):
        """우선순위에 따른 CSS 클래스 반환"""
        priority_classes = {
            'LOW': 'text-success',
            'MEDIUM': 'text-info',
            'HIGH': 'text-warning',
            'URGENT': 'text-danger',
        }
        return priority_classes.get(self.priority, 'text-secondary')
    
    def get_status_badge_class(self):
        """상태에 따른 배지 CSS 클래스 반환"""
        status_classes = {
            'TODO': 'bg-secondary',
            'IN_PROGRESS': 'bg-primary',
            'COMPLETED': 'bg-success',
            'CANCELLED': 'bg-dark',
        }
        return status_classes.get(self.status, 'bg-secondary')

class StudySession(models.Model):
    """학습 세션 모델"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_sessions')
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='study_sessions',
        verbose_name='관련 과제'
    )
    subject = models.ForeignKey(
        'timetable.Subject',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='study_sessions',
        verbose_name='관련 과목'
    )
    
    title = models.CharField(max_length=200, verbose_name='세션 제목')
    description = models.TextField(blank=True, verbose_name='학습 내용')
    
    # 시간 정보
    start_time = models.DateTimeField(verbose_name='시작 시간')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='종료 시간')
    duration_minutes = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(1440)],  # 최대 24시간
        verbose_name='소요시간(분)'
    )
    
    # 평가
    effectiveness_rating = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='효과성 평가(1-5)'
    )
    notes = models.TextField(blank=True, verbose_name='학습 노트')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '학습 세션'
        verbose_name_plural = '학습 세션들'
        ordering = ['-start_time']
        
    def __str__(self):
        return f"{self.title} ({self.start_time.strftime('%Y-%m-%d %H:%M')})"
    
    def save(self, *args, **kwargs):
        # 종료 시간이 있으면 소요시간 계산
        if self.start_time and self.end_time:
            duration = self.end_time - self.start_time
            self.duration_minutes = int(duration.total_seconds() / 60)
        super().save(*args, **kwargs)
    
    def get_duration_display(self):
        """소요시간을 시간:분 형식으로 반환"""
        if self.duration_minutes:
            hours = self.duration_minutes // 60
            minutes = self.duration_minutes % 60
            if hours > 0:
                return f"{hours}시간 {minutes}분"
            else:
                return f"{minutes}분"
        return "진행 중"

class Goal(models.Model):
    """학습 목표 모델"""
    
    GOAL_TYPE_CHOICES = [
        ('DAILY', '일일 목표'),
        ('WEEKLY', '주간 목표'),
        ('MONTHLY', '월간 목표'),
        ('SEMESTER', '학기 목표'),
        ('CUSTOM', '사용자 정의'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=200, verbose_name='목표 제목')
    description = models.TextField(blank=True, verbose_name='목표 설명')
    
    goal_type = models.CharField(
        max_length=10,
        choices=GOAL_TYPE_CHOICES,
        default='WEEKLY',
        verbose_name='목표 유형'
    )
    
    # 목표 기간
    start_date = models.DateField(verbose_name='시작일')
    end_date = models.DateField(verbose_name='종료일')
    
    # 메모
    memo = models.TextField(blank=True, verbose_name='메모')
    
    # 진행률 및 달성 여부
    progress = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='진행률(%)'
    )
    is_achieved = models.BooleanField(default=False, verbose_name='달성 여부')
    achievement_date = models.DateTimeField(null=True, blank=True, verbose_name='달성일시')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '목표'
        verbose_name_plural = '목표들'
        ordering = ['-start_date', '-created_at']
        
    def __str__(self):
        return f"{self.title} ({self.get_goal_type_display()})"
    
    def save(self, *args, **kwargs):
        # 진행률이 100%가 되면 자동으로 달성 상태로 변경
        if self.progress >= 100 and not self.is_achieved:
            self.is_achieved = True
            self.achievement_date = timezone.now()
        # 달성 상태로 변경되면 진행률을 100%로 설정
        elif self.is_achieved and self.progress < 100:
            self.progress = 100
            if not self.achievement_date:
                self.achievement_date = timezone.now()
        # 달성 상태가 아니면 달성일시 초기화
        elif not self.is_achieved:
            self.achievement_date = None
        super().save(*args, **kwargs)
    
    def get_progress_percentage(self):
        """진행률 반환"""
        return self.progress
    
    def update_progress_from_subgoals(self):
        """하위 목표 완료율에 따라 진행률 자동 계산 (사용자 정의 목표용)"""
        if self.goal_type == 'CUSTOM':
            subgoals = self.subgoals.all()
            if subgoals.exists():
                completed_count = subgoals.filter(is_completed=True).count()
                total_count = subgoals.count()
                self.progress = int((completed_count / total_count) * 100)
                self.save()
    
    def get_remaining_days(self):
        """남은 일수 반환"""
        today = timezone.now().date()
        if self.end_date > today:
            return (self.end_date - today).days
        return 0
    
    def is_overdue(self):
        """기한 초과 여부"""
        return timezone.now().date() > self.end_date and not self.is_achieved


class SubGoal(models.Model):
    """하위 목표 모델 (사용자 정의 목표용 체크리스트)"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    goal = models.ForeignKey(
        Goal,
        on_delete=models.CASCADE,
        related_name='subgoals',
        verbose_name='상위 목표'
    )
    title = models.CharField(max_length=200, verbose_name='하위 목표')
    description = models.TextField(blank=True, verbose_name='설명')
    
    # 완료 상태
    is_completed = models.BooleanField(default=False, verbose_name='완료 여부')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='완료일시')
    
    # 순서
    order = models.PositiveIntegerField(default=0, verbose_name='순서')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '하위 목표'
        verbose_name_plural = '하위 목표들'
        ordering = ['order', 'created_at']
    
    def __str__(self):
        status = '✓' if self.is_completed else '○'
        return f"{status} {self.title}"
    
    def save(self, *args, **kwargs):
        # 완료 상태 변경 시 완료일시 설정
        if self.is_completed and not self.completed_at:
            self.completed_at = timezone.now()
        elif not self.is_completed:
            self.completed_at = None
        super().save(*args, **kwargs)
        # 상위 목표 진행률 자동 업데이트
        self.goal.update_progress_from_subgoals()


class DailyPlanner(models.Model):
    """일일 플래너 모델"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_planners')
    date = models.DateField(verbose_name='날짜')
    
    # 하루 목표
    daily_goal = models.TextField(blank=True, verbose_name='오늘의 목표')
    
    # 총 학습시간 목표
    target_study_hours = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=8.0,
        validators=[MinValueValidator(0.1), MaxValueValidator(24.0)],
        verbose_name='목표 학습시간(시간)'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '일일 플래너'
        verbose_name_plural = '일일 플래너들'
        unique_together = ['user', 'date']
        ordering = ['-date']
        
    def __str__(self):
        return f"{self.user.username}의 {self.date} 플래너"


class TimeBlock(models.Model):
    """시간 블록 모델 (10분 단위)"""
    
    BLOCK_TYPE_CHOICES = [
        ('STUDY', '학습'),
        ('BREAK', '휴식'),
        ('MEAL', '식사'),
        ('EXERCISE', '운동'),
        ('OTHER', '기타'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    daily_planner = models.ForeignKey(
        DailyPlanner, 
        on_delete=models.CASCADE, 
        related_name='time_blocks'
    )
    
    # 시간 정보 (10분 단위)
    hour = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(23)],
        verbose_name='시간 (0-23)'
    )
    minute_block = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name='10분 블록 (0-5: 00,10,20,30,40,50분)'
    )
    
    # 블록 정보
    block_type = models.CharField(
        max_length=10,
        choices=BLOCK_TYPE_CHOICES,
        default='STUDY',
        verbose_name='블록 유형'
    )
    
    subject = models.ForeignKey(
        'timetable.Subject',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='time_blocks',
        verbose_name='관련 과목'
    )
    
    task = models.ForeignKey(
        Task,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='time_blocks',
        verbose_name='관련 과제'
    )
    
    # 색상 (과목 색상 또는 사용자 지정)
    color = models.CharField(
        max_length=7,
        default='#3498db',
        verbose_name='색상'
    )
    
    # 메모
    memo = models.CharField(max_length=100, blank=True, verbose_name='메모')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '시간 블록'
        verbose_name_plural = '시간 블록들'
        unique_together = ['daily_planner', 'hour', 'minute_block']
        ordering = ['hour', 'minute_block']
        
    def __str__(self):
        return f"{self.hour:02d}:{self.minute_block*10:02d} - {self.get_block_type_display()}"
    
    def get_time_display(self):
        """시간을 HH:MM 형식으로 반환"""
        return f"{self.hour:02d}:{self.minute_block*10:02d}"
    
    def get_end_time_display(self):
        """종료 시간을 HH:MM 형식으로 반환"""
        end_minute = (self.minute_block * 10) + 10
        if end_minute >= 60:
            return f"{self.hour+1:02d}:00"
        return f"{self.hour:02d}:{end_minute:02d}"


class TodoItem(models.Model):
    """일일 할 일 아이템"""
    STATUS_CHOICES = [
        ('pending', '대기중'),
        ('in_progress', '진행중'),
        ('completed', '완료'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', '낮음'),
        ('medium', '보통'),
        ('high', '높음'),
    ]
    
    SUBJECT_CHOICES = [
        ('math', '수학'),
        ('korean', '국어'),
        ('english', '영어'),
        ('history', '역사'),
        ('science', '과학'),
        ('military', '군사학'),
        ('physical', '체육'),
        ('other', '기타'),
    ]
    
    daily_planner = models.ForeignKey(DailyPlanner, on_delete=models.CASCADE, related_name='todo_items')
    title = models.CharField(max_length=200, verbose_name='할 일')
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, default='other', verbose_name='과목')
    description = models.TextField(blank=True, verbose_name='상세 설명')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='상태')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium', verbose_name='우선순위')
    estimated_time = models.PositiveIntegerField(null=True, blank=True, verbose_name='예상 소요시간(분)')
    order = models.PositiveIntegerField(default=0, verbose_name='순서')
    is_completed = models.BooleanField(default=False, verbose_name='완료 여부')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='완료 시간')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '할 일'
        verbose_name_plural = '할 일들'
        ordering = ['order', '-priority', 'created_at']
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # 완료 상태로 변경될 때 완료시간 설정
        if self.is_completed and not self.completed_at:
            self.completed_at = timezone.now()
        elif not self.is_completed:
            self.completed_at = None
        super().save(*args, **kwargs)
