from haystack import indexes

from .models import Package


class PackageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, use_template=True)
    pkg_type = indexes.CharField(model_attr='pkg_type', faceted=True)
    model = indexes.CharField(model_attr='get_model_name', faceted=True)
    name = indexes.CharField(model_attr='name')
    license = indexes.CharField(model_attr='license', faceted=True)
    is_active = indexes.BooleanField(model_attr='is_active')
    taxonomy = indexes.MultiValueField(faceted=True)

    def get_model(self):
        return Package

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(is_active=True)

    def prepare_taxonomy(self, obj):
        return [tag.name for tag in obj.tags.all()]

    def prepare_pkg_type(self, obj):
        return obj.get_pkg_type_display()
