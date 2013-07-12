from haystack import indexes
from .models import Project


class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, use_template=True)
    creator = indexes.CharField(model_attr='creator', faceted=True)
    countries = indexes.MultiValueField(faceted=True)
    model = indexes.CharField(model_attr='get_model_name', faceted=True)
    name = indexes.CharField(model_attr='name')
    is_active = indexes.BooleanField(model_attr='is_active')
    taxonomy = indexes.MultiValueField(faceted=True)

    def get_model(self):
        return Project

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(is_active=True)

    def prepare_countries(self, obj):
        return [country.name for country in obj.countries.all()]

    def prepare_taxonomy(self, obj):
        return [tag.name for tag in obj.tags.all()]
