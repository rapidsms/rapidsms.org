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
deny_projects.short_description = "Deny selected projects"


class ProjectAdmin(admin.ModelAdmin):
    actions = [publish_projects, deny_projects, ]
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'updated', 'status', 'feature')
    list_filter = ['created', 'updated', ]
    readonly_fields = ['created', 'updated', ]
    filter_horizontal = ('countries',)
    fieldsets = (
        (None,
            {'fields': ('created', 'updated', 'creator', 'name', 'slug',
                    'status', 'feature')},
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
        readonly_fields = self.readonly_fields
        # import pdb; pdb.set_trace()
        if obj:
            if obj.feature:
                return ['created', 'updated', 'feature']
        return ['created', 'updated', ]


admin.site.register(Project, ProjectAdmin)
