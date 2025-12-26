from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
import uuid

User = get_user_model()

class Category(models.Model):
    """커뮤니티 카테고리 모델"""
    
    CATEGORY_TYPES = [
        ('STUDY', '학습 자료'),
        ('EXAM', '시험 정보'),
        ('LECTURE', '강의 특성'),
        ('FITNESS', '체력평가'),
        ('ENGLISH', '영어상식'),
        ('PROJECT', '프로젝트'),
        ('QNA', '질문답변'),
        ('FREE', '자유게시판'),
        ('NOTICE', '공지사항'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, verbose_name='카테고리명')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='슬러그')
    category_type = models.CharField(
        max_length=10,
        choices=CATEGORY_TYPES,
        default='FREE',
        verbose_name='카테고리 유형'
    )
    description = models.TextField(blank=True, verbose_name='설명')
    icon = models.CharField(max_length=50, default='fas fa-comments', verbose_name='아이콘')
    color = models.CharField(max_length=7, default='#007bff', verbose_name='색상')
    is_active = models.BooleanField(default=True, verbose_name='활성화')
    order = models.IntegerField(default=0, verbose_name='정렬순서')
    
    # 권한 설정
    department_restricted = models.BooleanField(default=False, verbose_name='학과 제한')
    allowed_departments = models.JSONField(default=list, blank=True, verbose_name='허용 학과')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '카테고리'
        verbose_name_plural = '카테고리들'
        ordering = ['order', 'name']
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('community:category_posts', kwargs={'slug': self.slug})
    
    def get_post_count(self):
        return self.posts.filter(is_active=True).count()

class Post(models.Model):
    """게시글 모델"""
    
    POST_TYPES = [
        ('NORMAL', '일반'),
        ('NOTICE', '공지'),
        ('URGENT', '긴급'),
        ('QUESTION', '질문'),
        ('RESOURCE', '자료'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='작성자')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts', verbose_name='카테고리')
    
    title = models.CharField(max_length=200, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    post_type = models.CharField(
        max_length=10,
        choices=POST_TYPES,
        default='NORMAL',
        verbose_name='게시글 유형'
    )
    
    # 메타 정보
    views = models.PositiveIntegerField(default=0, verbose_name='조회수')
    likes = models.ManyToManyField(User, blank=True, related_name='liked_posts', verbose_name='좋아요')
    bookmarks = models.ManyToManyField(User, blank=True, related_name='bookmarked_posts', verbose_name='북마크')
    is_pinned = models.BooleanField(default=False, verbose_name='상단 고정')
    is_active = models.BooleanField(default=True, verbose_name='활성화')
    
    # 연관 정보
    subject = models.ForeignKey(
        'timetable.Subject',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='community_posts',
        verbose_name='관련 과목'
    )
    
    # 태그
    tags = models.JSONField(default=list, blank=True, verbose_name='태그')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '게시글'
        verbose_name_plural = '게시글들'
        ordering = ['-is_pinned', '-created_at']
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('community:post_detail', kwargs={'pk': self.pk})
    
    def get_like_count(self):
        return self.likes.count()
    
    def get_comment_count(self):
        return self.comments.filter(is_active=True).count()
    
    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])
    
    def is_liked_by(self, user):
        return self.likes.filter(id=user.id).exists() if user.is_authenticated else False
    
    def is_bookmarked_by(self, user):
        return self.bookmarks.filter(id=user.id).exists() if user.is_authenticated else False
    
    def get_bookmark_count(self):
        return self.bookmarks.count()

class Comment(models.Model):
    """댓글 모델"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='게시글')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='작성자')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name='부모 댓글'
    )
    
    content = models.TextField(verbose_name='내용')
    is_active = models.BooleanField(default=True, verbose_name='활성화')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글들'
        ordering = ['created_at']
        
    def __str__(self):
        return f"{self.post.title} - {self.author.username}"
    
    def get_reply_count(self):
        return self.replies.filter(is_active=True).count()

class Attachment(models.Model):
    """첨부파일 모델"""
    
    FILE_TYPES = [
        ('IMAGE', '이미지'),
        ('DOCUMENT', '문서'),
        ('ARCHIVE', '압축파일'),
        ('OTHER', '기타'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='attachments', verbose_name='게시글')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='업로더')
    
    file = models.FileField(upload_to='community/attachments/%Y/%m/', verbose_name='파일')
    original_name = models.CharField(max_length=255, verbose_name='원본 파일명')
    file_type = models.CharField(
        max_length=10,
        choices=FILE_TYPES,
        default='OTHER',
        verbose_name='파일 유형'
    )
    file_size = models.PositiveIntegerField(verbose_name='파일 크기(bytes)')
    download_count = models.PositiveIntegerField(default=0, verbose_name='다운로드 수')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = '첨부파일'
        verbose_name_plural = '첨부파일들'
        ordering = ['-created_at']
        
    def __str__(self):
        return self.original_name
    
    def get_file_size_display(self):
        """파일 크기를 읽기 쉬운 형태로 반환"""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def increment_download(self):
        self.download_count += 1
        self.save(update_fields=['download_count'])

class Report(models.Model):
    """신고 모델"""
    
    REPORT_TYPES = [
        ('SPAM', '스팸'),
        ('INAPPROPRIATE', '부적절한 내용'),
        ('HARASSMENT', '괴롭힘'),
        ('COPYRIGHT', '저작권 침해'),
        ('OTHER', '기타'),
    ]
    
    REPORT_STATUS = [
        ('PENDING', '대기중'),
        ('REVIEWING', '검토중'),
        ('RESOLVED', '해결됨'),
        ('REJECTED', '기각됨'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports', verbose_name='신고자')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reports',
        verbose_name='신고된 게시글'
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reports',
        verbose_name='신고된 댓글'
    )
    
    report_type = models.CharField(
        max_length=15,
        choices=REPORT_TYPES,
        verbose_name='신고 유형'
    )
    reason = models.TextField(verbose_name='신고 사유')
    status = models.CharField(
        max_length=10,
        choices=REPORT_STATUS,
        default='PENDING',
        verbose_name='처리 상태'
    )
    
    # 관리자 처리 정보
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_reports',
        verbose_name='처리자'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True, verbose_name='처리일시')
    admin_note = models.TextField(blank=True, verbose_name='관리자 메모')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '신고'
        verbose_name_plural = '신고들'
        ordering = ['-created_at']
        
    def __str__(self):
        target = self.post.title if self.post else self.comment.content[:50]
        return f"{self.get_report_type_display()} - {target}"
