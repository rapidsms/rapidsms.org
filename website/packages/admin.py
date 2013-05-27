from django.contrib import admin

from .models import Package


class PackageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Package, PackageAdmin)
