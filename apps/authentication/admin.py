from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserPreferences


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom User Admin
    """
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_admin', 'is_active', 'date_joined')
    list_filter = ('is_admin', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'bio', 'profile_image')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_admin', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ('date_joined', 'last_login')


@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    """
    User Preferences Admin
    """
    list_display = ('user', 'email_notifications', 'created_at', 'updated_at')
    list_filter = ('email_notifications', 'created_at')
    search_fields = ('user__email', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {'fields': ('user',)}),
        ('Preferences', {
            'fields': ('favorite_genres', 'preferred_languages', 'email_notifications'),
        }),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
