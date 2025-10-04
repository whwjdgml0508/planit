from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Post, Comment, Attachment, Report

class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0
    readonly_fields = ['file_size', 'download_count', 'created_at']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_type', 'get_post_count', 'is_active', 'order', 'created_at']
    list_filter = ['category_type', 'is_active', 'department_restricted']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('name', 'slug', 'category_type', 'description')
        }),
        ('디자인', {
            'fields': ('icon', 'color', 'order')
        }),
        ('권한 설정', {
            'fields': ('is_active', 'department_restricted', 'allowed_departments')
        }),
        ('메타데이터', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_post_count(self, obj):
        return obj.get_post_count()
    get_post_count.short_description = '게시글 수'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'post_type', 'views', 'get_like_count', 
                   'get_comment_count', 'is_pinned', 'is_active', 'created_at']
    list_filter = ['category', 'post_type', 'is_pinned', 'is_active', 'created_at']
    search_fields = ['title', 'content', 'author__username', 'tags']
    readonly_fields = ['id', 'views', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    inlines = [AttachmentInline]
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('author', 'category', 'title', 'content')
        }),
        ('분류', {
            'fields': ('post_type', 'subject', 'tags')
        }),
        ('설정', {
            'fields': ('is_pinned', 'is_active')
        }),
        ('통계', {
            'fields': ('views',),
            'classes': ('collapse',)
        }),
        ('메타데이터', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_like_count(self, obj):
        return obj.get_like_count()
    get_like_count.short_description = '좋아요'
    
    def get_comment_count(self, obj):
        return obj.get_comment_count()
    get_comment_count.short_description = '댓글'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'category', 'subject')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['get_post_title', 'author', 'get_content_preview', 'parent', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['content', 'author__username', 'post__title']
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('post', 'author', 'parent', 'content')
        }),
        ('설정', {
            'fields': ('is_active',)
        }),
        ('메타데이터', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_post_title(self, obj):
        return obj.post.title
    get_post_title.short_description = '게시글'
    
    def get_content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    get_content_preview.short_description = '내용 미리보기'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'post', 'parent')

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['original_name', 'get_post_title', 'uploader', 'file_type', 
                   'get_file_size', 'download_count', 'created_at']
    list_filter = ['file_type', 'created_at']
    search_fields = ['original_name', 'post__title', 'uploader__username']
    readonly_fields = ['id', 'file_size', 'download_count', 'created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('post', 'uploader', 'file', 'original_name')
        }),
        ('파일 정보', {
            'fields': ('file_type', 'file_size')
        }),
        ('통계', {
            'fields': ('download_count',)
        }),
        ('메타데이터', {
            'fields': ('id', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_post_title(self, obj):
        return obj.post.title
    get_post_title.short_description = '게시글'
    
    def get_file_size(self, obj):
        return obj.get_file_size_display()
    get_file_size.short_description = '파일 크기'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('post', 'uploader')

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['get_target', 'reporter', 'report_type', 'status', 'reviewed_by', 'created_at']
    list_filter = ['report_type', 'status', 'created_at']
    search_fields = ['reason', 'reporter__username', 'post__title', 'comment__content']
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('신고 정보', {
            'fields': ('reporter', 'post', 'comment', 'report_type', 'reason')
        }),
        ('처리 정보', {
            'fields': ('status', 'reviewed_by', 'reviewed_at', 'admin_note')
        }),
        ('메타데이터', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_target(self, obj):
        if obj.post:
            return format_html('<strong>게시글:</strong> {}', obj.post.title)
        elif obj.comment:
            return format_html('<strong>댓글:</strong> {}', obj.comment.content[:30] + '...')
        return '-'
    get_target.short_description = '신고 대상'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('reporter', 'post', 'comment', 'reviewed_by')
    
    actions = ['mark_as_resolved', 'mark_as_rejected']
    
    def mark_as_resolved(self, request, queryset):
        queryset.update(status='RESOLVED', reviewed_by=request.user)
        self.message_user(request, f'{queryset.count()}개의 신고가 해결됨으로 처리되었습니다.')
    mark_as_resolved.short_description = '선택된 신고를 해결됨으로 처리'
    
    def mark_as_rejected(self, request, queryset):
        queryset.update(status='REJECTED', reviewed_by=request.user)
        self.message_user(request, f'{queryset.count()}개의 신고가 기각됨으로 처리되었습니다.')
    mark_as_rejected.short_description = '선택된 신고를 기각됨으로 처리'
