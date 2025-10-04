from django.contrib import admin
from .models import Subject, TimeSlot, Semester

class TimeSlotInline(admin.TabularInline):
    model = TimeSlot
    extra = 1
    fields = ['day', 'period', 'location', 'note']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'professor', 'credits', 'subject_type', 'user', 'created_at']
    list_filter = ['subject_type', 'credits', 'created_at']
    search_fields = ['name', 'professor', 'user__username']
    readonly_fields = ['id', 'created_at', 'updated_at']
    inlines = [TimeSlotInline]
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('user', 'name', 'professor', 'credits')
        }),
        ('분류 및 평가', {
            'fields': ('subject_type', 'evaluation_method')
        }),
        ('추가 정보', {
            'fields': ('classroom', 'note', 'color')
        }),
        ('메타데이터', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['subject', 'day', 'period', 'location', 'get_user']
    list_filter = ['day', 'period', 'subject__subject_type']
    search_fields = ['subject__name', 'subject__user__username', 'location']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    def get_user(self, obj):
        return obj.subject.user.username
    get_user.short_description = '사용자'

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['user', 'year', 'semester', 'is_current', 'start_date', 'end_date']
    list_filter = ['year', 'semester', 'is_current']
    search_fields = ['user__username']
    readonly_fields = ['id', 'created_at', 'updated_at']
