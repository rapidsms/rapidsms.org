from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User


class UserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    save_on_top = True
    list_display = ('email', 'name', 'is_staff', 'user_type')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_type')
    search_fields = ('email', 'name')
    ordering = ('email',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('user_type', 'name',
                'location', 'country', 'for_hire')}),
        ('Websites', {'fields': ('website_url', 'github_url')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(User, UserAdmin)
