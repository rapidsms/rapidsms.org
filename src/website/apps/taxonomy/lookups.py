from selectable.base import ModelLookup
from selectable.registry import registry

from .models import Taxonomy


class TaxonomyLookup(ModelLookup):
    model = Taxonomy
    search_fields = ('name__icontains', )


registry.register(TaxonomyLookup)
