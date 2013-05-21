from django.contrib import admin

from .models import Country, Package


class PackageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Package, PackageAdmin)
admin.site.register(Country)
