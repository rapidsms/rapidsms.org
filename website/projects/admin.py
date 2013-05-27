from django.contrib import admin

from .models import Country, Project


class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Project, ProjectAdmin)
admin.site.register(Country)
