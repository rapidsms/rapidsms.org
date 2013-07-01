from haystack import indexes
from .models import Project


class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, use_template=True)
    creator = indexes.CharField(model_attr='creator', faceted=True)
    countries = indexes.MultiValueField(faceted=True)
    model = indexes.CharField(model_attr='get_model_name', faceted=True)
    name = indexes.CharField(model_attr='name')
    is_active = indexes.BooleanField(model_attr='is_active')

    def get_model(self):
        return Project

    def prepare_countries(self, obj):
        return [country.name for country in obj.countries.all()]
