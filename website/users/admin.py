from django.contrib import admin
from django.contrib.auth import admin as auth

from .forms import UserChangeForm, UserCreationForm
from .models import User


class UserAdmin(auth.UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    list_display = ('email', 'name', 'is_staff', 'user_type')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_type')
    ordering = ('email',)
    save_on_top = True
    search_fields = ('email', 'name')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('user_type', 'name',
                'location', 'country', 'website_url', 'github_url',
                'for_hire')}),
        ('Avatar Options', {'fields': ('gravatar_email', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(User, UserAdmin)
