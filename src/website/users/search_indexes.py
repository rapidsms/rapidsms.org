import json

from haystack import indexes
from .models import User


class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, use_template=True)
    model = indexes.CharField(model_attr='get_model_name', faceted=True)
    for_hire = indexes.CharField(model_attr='for_hire', faceted=True)
    name = indexes.CharField(model_attr='name')
    countries = indexes.CharField(model_attr='country', faceted=True, null=True)
    user_type = indexes.CharField(model_attr='user_type', faceted=True)
    is_active = indexes.BooleanField(model_attr='is_active')

    def get_model(self):
        return User

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(is_active=True)

    def prepare_for_hire(self, obj):
        return 'Yes' if obj.for_hire else 'No'

    def prepare_user_type(self, obj):
        return obj.get_user_type_display()

    # def toJson(self):
    #     return json.dumps(self.__dict__)

    def __repr__(self):
        return self.toJson()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
