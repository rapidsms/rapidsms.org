from django.contrib import admin

from .models import Country, Project


def publish_projects(modeladmin, request, queryset):
    """Set project status to published"""
    queryset.update(status=Project.PUBLISHED)
publish_projects.short_description = "Publish selected projects"


def deny_projects(modeladmin, request, queryset):
    """Set project status to denied"""
    queryset.update(status=Project.DENIED)
deny_projects.short_description = "Deny selected projects"


class ProjectAdmin(admin.ModelAdmin):
    actions = [publish_projects, deny_projects, ]
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'updated', 'status')
    list_filter = ('status',)
    readonly_fields = ('created', 'updated')
    filter_horizontal = ('countries',)
    fieldsets = (
        (None,
            {'fields': ('created', 'updated', 'creator', 'name', 'slug',
                    'status')},
        ),
        ('Project Information',
            {'fields': ('started', 'countries', 'description', 'challenges',
                    'audience', 'technologies', 'metrics', 'num_users',
                    'repository_url', 'packages', 'tags')},
        ),
    )


admin.site.register(Project, ProjectAdmin)
admin.site.register(Country)
