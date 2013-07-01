from django.contrib import admin

from .models import Package


class PackageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'pkg_type', 'updated', 'pypi_updated', 'is_active')
    list_filter = ('pkg_type', 'is_active')
    readonly_fields = ('created', 'updated', 'pypi_updated', 'pypi_json',
            'author_name', 'author_email', 'maintainer_name',
            'maintainer_email', 'version', 'summary', 'release_date')
    fieldsets = (
        (None,
            {'fields': ('created', 'updated', 'creator', 'pkg_type', 'name',
                    'slug', 'is_active')},
        ),
        ('URLs',
            {'fields': ('docs_url', 'tests_url', 'repo_url', 'home_url')},
        ),
        ('PyPI Information',
            {'fields': ('pypi_updated', 'pypi_json', 'author_name',
                    'author_email', 'maintainer_name', 'maintainer_email',
                    'version', 'summary', 'release_date')},
        ),
    )


admin.site.register(Package, PackageAdmin)
