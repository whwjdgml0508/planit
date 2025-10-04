from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    """확장된 사용자 모델"""
    
    DEPARTMENT_CHOICES = [
        ('AERO', '항공우주공학과'),
        ('MECH', '기계공학과'),
        ('ELEC', '전자공학과'),
        ('COMP', '컴퓨터공학과'),
        ('CIVIL', '토목공학과'),
        ('CHEM', '화학공학과'),
        ('MATH', '수학과'),
        ('PHYS', '물리학과'),
        ('ENG', '영어영문학과'),
        ('OTHER', '기타'),
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
        max_length=10, 
        choices=DEPARTMENT_CHOICES,
        default='OTHER',
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
        validators=[RegexValidator(r'^\d{3}-\d{4}-\d{4}$', '전화번호 형식: 010-1234-5678')],
        verbose_name='전화번호'
    )
    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True,
        verbose_name='프로필 이미지'
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='자기소개'
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
            'AERO': '항공',
            'MECH': '기계',
            'ELEC': '전자',
            'COMP': '컴공',
            'CIVIL': '토목',
            'CHEM': '화공',
            'MATH': '수학',
            'PHYS': '물리',
            'ENG': '영문',
            'OTHER': '기타',
        }
        return dept_short.get(self.department, '기타')
