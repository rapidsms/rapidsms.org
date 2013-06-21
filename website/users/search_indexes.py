from haystack import indexes
from .models import User


class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, use_template=True)
    model = indexes.CharField(model_attr='get_model_name', faceted=True)

    def get_model(self):
        return User
