from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import RapidSMSAdminUserChangeForm, RapidSMSAdminUserCreationForm
from .models import User


class RapidSMSUserAdmin(UserAdmin):
    form = RapidSMSAdminUserChangeForm
    add_form = RapidSMSAdminUserCreationForm
    save_on_top = True
    list_display = list(UserAdmin.list_display) + ['user_type']
    list_filter = list(UserAdmin.list_filter) + ['user_type']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('user_type', 'first_name', 'last_name',
                'email', 'location', 'country', 'for_hire')}),
        ('Websites', {'fields': ('website_url', 'github_url')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(User, RapidSMSUserAdmin)
