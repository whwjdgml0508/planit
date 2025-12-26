from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    """확장된 사용자 모델"""
    
    DEPARTMENT_CHOICES = [
        ('INTL', '국제관계학과'),
        ('DEFENSE', '국방경영학과'),
        ('AERO_POLICY', '항공우주정책학과'),
        ('COMP', '컴퓨터과학과'),
        ('AERO', '항공공학과'),
        ('SPACE', '우주공학과'),
        ('MECH', '기계공학과'),
        ('ELEC', '전자통신공학과'),
        ('SYSTEM', '시스템공학과'),
    ]
    
    GRADE_CHOICES = [
        (1, '1학년'),
        (2, '2학년'),
        (3, '3학년'),
        (4, '4학년'),
    ]
    
    
    # 추가 필드
    student_id = models.CharField(
        max_length=10, 
        unique=True, 
        validators=[RegexValidator(r'^\d{7}$', '학번은 7자리 숫자여야 합니다.')],
        help_text='7자리 학번을 입력하세요'
    )
    department = models.CharField(
        max_length=15, 
        choices=DEPARTMENT_CHOICES,
        default='COMP',
        verbose_name='학과'
    )
    grade = models.IntegerField(
        choices=GRADE_CHOICES,
        default=1,
        verbose_name='학년'
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name='전화번호'
    )
    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True,
        verbose_name='프로필 이미지'
    )
    # avatar_choice 필드는 더 이상 사용하지 않음 (legacy, 마이그레이션 호환성 유지)
    avatar_choice = models.CharField(
        max_length=20,
        default='default',
        blank=True,
        verbose_name='아바타 선택 (legacy)'
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='자기소개'
    )
    weekly_study_goal = models.PositiveIntegerField(
        default=40,
        verbose_name='주간 학습 목표(시간)'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = '사용자들'
        
    def __str__(self):
        return f"{self.username} ({self.student_id})"
    
    def get_full_name(self):
        return f"{self.last_name}{self.first_name}"
    
    def get_department_display_short(self):
        """학과명 축약형 반환"""
        dept_short = {
            'INTL': '국관',
            'DEFENSE': '국경',
            'AERO_POLICY': '항정',
            'COMP': '컴과',
            'AERO': '항공',
            'SPACE': '우주',
            'MECH': '기계',
            'ELEC': '전통',
            'SYSTEM': '시공',
        }
        return dept_short.get(self.department, '기타')
    
    def get_avatar_url(self):
        """프로필 이미지 URL 또는 기본 아이콘 반환"""
        if self.profile_image:
            return self.profile_image.url
        return '👤'
    
    def get_avatar_emoji(self):
        """기본 프로필 아이콘 반환"""
        return '👤'
