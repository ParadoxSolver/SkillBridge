from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'college_name', 'is_verified', 'trust_score', 'total_earnings', 'date_joined')
    list_filter = ('is_verified', 'is_staff', 'is_active', 'college_name')
    search_fields = ('username', 'email', 'college_name', 'skills')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('SkillBridge Profile', {
            'fields': ('college_email', 'college_name', 'is_verified', 'bio', 'avatar', 'skills'),
        }),
        ('Trust & Earnings', {
            'fields': ('trust_score', 'total_earnings', 'total_spent'),
        }),
    )
