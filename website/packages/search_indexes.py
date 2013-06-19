from haystack import indexes
from .models import Package


class PackageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, use_template=True)
    creator = indexes.CharField(model_attr='creator', faceted=True)
    pkg_type = indexes.CharField(model_attr='pkg_type', faceted=True)
    model = indexes.CharField(model_attr='get_model_name', faceted=True)

    def get_model(self):
        return Package

    def prepare_pkg_type(self, obj):
        return Package.PACKAGE_TYPES[obj.pkg_type]
