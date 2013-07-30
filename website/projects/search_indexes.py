from haystack import indexes

from .models import Project


class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, use_template=True)
    creator = indexes.CharField(model_attr='creator', faceted=True)
    countries = indexes.MultiValueField(faceted=True)
    # description = indexes.
    model = indexes.CharField(model_attr='get_model_name', faceted=True)
    name = indexes.CharField(model_attr='name')
    description = indexes.CharField(model_attr="description")
    taxonomy = indexes.MultiValueField(faceted=True)
    collaborators = indexes.MultiValueField(faceted=True)
    status = indexes.CharField(model_attr='status')
    num_users = indexes.CharField(model_attr='num_users', faceted=True)

    def get_model(self):
        return Project

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(status=Project.PUBLISHED)

    def prepare_countries(self, obj):
        return [country.name for country in obj.countries.all()]

    def display_countries(self):
        """Display countries as a comma-separated list."""
        total = self.countries.count()
        result = ''
        for index, country in enumerate(self.countries.all(), 1):
            if index == total and index != 1:
                result += 'and '
            result += str(country)
            if index != total:
                result += ', ' if total > 2 else ' '
        return result

    def prepare_num_users(self, obj):
        return obj.get_num_users_display()

    def prepare_taxonomy(self, obj):
        return [tag.name for tag in obj.tags.all()]

    def prepare_collaborators(self, obj):
        return [user.name for user in obj.collaborators.all()]
