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
        # 완료 상태로 변경될 때 완료일시 설정
        if self.status == 'COMPLETED' and not self.completed_at:
            self.completed_at = timezone.now()
            self.progress = 100
        elif self.status != 'COMPLETED':
            self.completed_at = None
            
        super().save(*args, **kwargs)
    
    def is_overdue(self):
        """마감일이 지났는지 확인"""
        if self.due_date and self.status != 'COMPLETED':
            return timezone.now() > self.due_date
        return False
    
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
    
    # 목표 수치
    target_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.1), MaxValueValidator(999.99)],
        verbose_name='목표 학습시간(시간)'
    )
    target_tasks = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(1000)],
        verbose_name='목표 과제 수'
    )
    
    # 달성 여부
    is_achieved = models.BooleanField(default=False, verbose_name='달성 여부')
    achievement_date = models.DateTimeField(null=True, blank=True, verbose_name='달성일시')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '학습 목표'
        verbose_name_plural = '학습 목표들'
        ordering = ['-start_date', '-created_at']
        
    def __str__(self):
        return f"{self.title} ({self.get_goal_type_display()})"
    
    def get_progress_percentage(self):
        """목표 달성률 계산"""
        if not self.target_hours and not self.target_tasks:
            return 0
            
        progress = 0
        total_weight = 0
        
        if self.target_hours:
            # 해당 기간의 실제 학습시간 계산
            actual_hours = self.user.study_sessions.filter(
                start_time__date__gte=self.start_date,
                start_time__date__lte=self.end_date,
                end_time__isnull=False
            ).aggregate(
                total=models.Sum('duration_minutes')
            )['total'] or 0
            
            actual_hours = actual_hours / 60  # 분을 시간으로 변환
            hours_progress = min(100, (actual_hours / float(self.target_hours)) * 100)
            progress += hours_progress
            total_weight += 1
        
        if self.target_tasks:
            # 해당 기간의 완료된 과제 수 계산
            completed_tasks = self.user.tasks.filter(
                completed_at__date__gte=self.start_date,
                completed_at__date__lte=self.end_date,
                status='COMPLETED'
            ).count()
            
            tasks_progress = min(100, (completed_tasks / self.target_tasks) * 100)
            progress += tasks_progress
            total_weight += 1
        
        return int(progress / total_weight) if total_weight > 0 else 0
