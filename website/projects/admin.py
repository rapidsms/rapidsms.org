from django.contrib import admin

from .models import Project
from .forms import ProjectAdminForm


def publish_projects(modeladmin, request, queryset):
    """Set project status to published"""
    for project in queryset:
        project.change_status(Project.PUBLISHED)
        project.save()
publish_projects.short_description = "Publish selected projects"


def deny_projects(modeladmin, request, queryset):
    """Set project status to denied"""
    for project in queryset:
        project.change_status(Project.DENIED)
        project.save()
deny_projects.short_description = "Deny publication of selected projects"


class ProjectAdmin(admin.ModelAdmin):
    actions = [publish_projects, deny_projects, ]
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'updated', 'status', 'feature')
    list_filter = ['created', 'updated', ]
    search_fields = ['name', ]
    readonly_fields = ['created', 'updated', 'status', ]
    filter_horizontal = ('countries', 'collaborators')
    fieldsets = (
        (None,
            {'fields': ('created', 'updated', 'creator', 'collaborators',
                        'name', 'slug', 'status', 'feature')},
        ),
        ('Project Information',
            {'fields': ('started', 'countries', 'description', 'challenges',
                    'audience', 'technologies', 'metrics', 'num_users',
                    'repository_url', 'packages', 'tags')},
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        """
        Hook for specifying custom readonly fields.
        """
        if obj:
            if obj.feature:
                return ['created', 'updated', 'status', 'feature']
        return ['created', 'updated', 'status', ]


admin.site.register(Project, ProjectAdmin)
