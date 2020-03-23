from django.contrib import admin

from .models import Taxonomy


class TaxonomyAdmin(admin.ModelAdmin):
    list_display = ('name', )


admin.site.register(Taxonomy, TaxonomyAdmin)
