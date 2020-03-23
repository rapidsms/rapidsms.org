import json

from django.views.generic import TemplateView
from website.projects.models import Project

MODEL_FACETS = {
    'package': ('pkg_type', 'license', 'taxonomy',),
    'project': ('countries', 'taxonomy', 'collaborators', 'num_users'),
    'user': ('countries', 'for_hire', 'user_type'),
}


class Home(TemplateView):
    template_name = 'website/home.html'

    @staticmethod
    def get_map_data(project, countries):
        scope = countries[0].scope
        map_data = {country.code: project.get_map_data(country)
                    for country in countries}
        data = {
            'map_data': json.dumps(map_data),
            'scope': json.dumps(scope.json_serializable()),
        }
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        feature_project = Project.objects.get_feature_project()
        context.update({'feature_project': feature_project})
        if feature_project:
            countries = feature_project.countries.all()
            map_data = self.get_map_data(feature_project, countries)
            context.update(map_data)
        return context


class About(TemplateView):
    template_name = 'website/about.html'


class Community(TemplateView):
    template_name = 'website/community.html'


class Help(TemplateView):
    template_name = 'website/help.html'


class Ecosystem(TemplateView):
    template_name = 'website/ecosystem.html'
