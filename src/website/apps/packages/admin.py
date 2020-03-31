from django.contrib import admin

from .models import Package


class PackageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'pkg_type', 'updated', 'pypi_updated', 'is_active', 'is_flagged')
    list_filter = ('pkg_type', 'is_active')
    readonly_fields = ('created', 'updated', 'pypi_updated', 'pypi_json',
                       'author_name', 'author_email', 'maintainer_name',
                       'maintainer_email', 'version', 'summary', 'release_date',
                       'license', 'docs_url', 'home_url')
    fieldsets = (
        (None,
            {'fields': ('created', 'updated', 'creator', 'pkg_type', 'name', 'slug', 'is_active', 'is_flagged')},
         ),
        ('URLs',
            {'fields': ('tests_url', 'repo_url')},
         ),
        ('PyPI Information',
            {'fields': ('pypi_updated', 'pypi_json', 'author_name',
                        'author_email', 'maintainer_name', 'maintainer_email',
                        'version', 'summary', 'release_date', 'license',
                        'docs_url', 'home_url')},
         ),
    )


admin.site.register(Package, PackageAdmin)
