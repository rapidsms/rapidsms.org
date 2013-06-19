from haystack import indexes
from .models import Package


class PackageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    creator = indexes.CharField(model_attr='creator', faceted=True)

    def get_model(self):
        return Package
