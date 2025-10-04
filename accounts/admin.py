from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.utils.html import format_html

User = get_user_model()

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """사용자 관리자 페이지"""
    
    list_display = ('username', 'student_id', 'get_full_name', 'department', 'grade', 
                   'email', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('department', 'grade', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'student_id', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('추가 정보', {
            'fields': ('student_id', 'department', 'grade', 'phone_number', 
                      'profile_image', 'bio')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('추가 정보', {
            'fields': ('first_name', 'last_name', 'email', 'student_id', 
                      'department', 'grade', 'phone_number')
        }),
    )
    
    def get_full_name(self, obj):
        return obj.get_full_name() or '-'
    get_full_name.short_description = '이름'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()
