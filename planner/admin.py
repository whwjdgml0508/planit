from django.contrib import admin
from django.utils.html import format_html
from .models import Task, StudySession, Goal

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'priority', 'status', 'due_date', 'progress', 'created_at']
    list_filter = ['category', 'priority', 'status', 'created_at', 'due_date']
    search_fields = ['title', 'description', 'user__username']
    readonly_fields = ['id', 'created_at', 'updated_at', 'completed_at']
    date_hierarchy = 'due_date'
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('user', 'title', 'description')
        }),
        ('분류 및 상태', {
            'fields': ('category', 'priority', 'status', 'progress')
        }),
        ('시간 관리', {
            'fields': ('due_date', 'estimated_hours', 'actual_hours')
        }),
        ('연관 정보', {
            'fields': ('subject',)
        }),
        ('메타데이터', {
            'fields': ('id', 'created_at', 'updated_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'subject')

@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'get_task_title', 'get_subject_name', 'start_time', 'get_duration', 'effectiveness_rating']
    list_filter = ['start_time', 'effectiveness_rating', 'task__category']
    search_fields = ['title', 'description', 'user__username', 'task__title']
    readonly_fields = ['id', 'duration_minutes', 'created_at', 'updated_at']
    date_hierarchy = 'start_time'
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('user', 'title', 'description')
        }),
        ('연관 정보', {
            'fields': ('task', 'subject')
        }),
        ('시간 정보', {
            'fields': ('start_time', 'end_time', 'duration_minutes')
        }),
        ('평가', {
            'fields': ('effectiveness_rating', 'notes')
        }),
        ('메타데이터', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_task_title(self, obj):
        return obj.task.title if obj.task else '-'
    get_task_title.short_description = '관련 과제'
    
    def get_subject_name(self, obj):
        return obj.subject.name if obj.subject else '-'
    get_subject_name.short_description = '관련 과목'
    
    def get_duration(self, obj):
        return obj.get_duration_display()
    get_duration.short_description = '소요시간'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'task', 'subject')

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'goal_type', 'start_date', 'end_date', 'get_progress', 'is_achieved']
    list_filter = ['goal_type', 'is_achieved', 'start_date', 'end_date']
    search_fields = ['title', 'description', 'user__username']
    readonly_fields = ['id', 'created_at', 'updated_at', 'achievement_date']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('user', 'title', 'description', 'goal_type')
        }),
        ('기간', {
            'fields': ('start_date', 'end_date')
        }),
        ('목표 수치', {
            'fields': ('target_hours', 'target_tasks')
        }),
        ('달성 정보', {
            'fields': ('is_achieved', 'achievement_date')
        }),
        ('메타데이터', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_progress(self, obj):
        progress = obj.get_progress_percentage()
        color = 'green' if progress >= 80 else 'orange' if progress >= 50 else 'red'
        return format_html(
            '<span style="color: {};">{:d}%</span>',
            color,
            progress
        )
    get_progress.short_description = '진행률'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
