from selectable.base import ModelLookup
from selectable.registry import registry

from .models import Package


class PackageLookup(ModelLookup):
    model = Package
    search_fields = ('name__icontains',)

registry.register(PackageLookup)
