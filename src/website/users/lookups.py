from selectable.base import ModelLookup
from selectable.registry import registry

from .models import User


class UserLookup(ModelLookup):
    model = User
    search_fields = ('email__icontains', 'name__icontains')


registry.register(UserLookup)
