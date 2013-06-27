from haystack import indexes
from .models import User


class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, use_template=True)
    model = indexes.CharField(model_attr='get_model_name', faceted=True)
    for_hire = indexes.CharField(model_attr='for_hire', faceted=True)
    name = indexes.CharField(model_attr='name')
    countries = indexes.CharField(model_attr='country', faceted=True, null=True)

    def get_model(self):
        return User

    def prepare_for_hire(self, obj):
        return 'Yes' if obj.for_hire else 'No'
