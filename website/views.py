import json

from django.http import Http404
from django.views.generic import TemplateView

from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView, search_view_factory

from website.projects.models import Project

from .forms import FacetedSearchListingForm


MODEL_FACETS = {
    'package': ('pkg_type', 'license'),
    'project': ('countries', 'creator', 'taxonomy', 'collaborators',
        'num_users'),
    'user': ('countries', 'for_hire', 'user_type'),
}


class Home(TemplateView):
    template_name = 'website/home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        map_data = {}
        # TODO: refactor the logic to get N project per country
        # Add Caching!
        projects = Project.objects.all()
        for project in projects:
            data = {'name': project.name,
                     'description': project.description,
                     'fillKey': 'project',}
            for country in project.countries.all():
                map_data[country.code] = data
        context.update({
            'map_data_json':  json.dumps(map_data)
        })
        return context


class About(TemplateView):
    template_name = 'website/about.html'


class Help(TemplateView):
    template_name = 'website/help.html'


class FacetedSearchListingView(FacetedSearchView):

    def clean_filters(self):
        "Returns a list of tuples (filter, value) of applied facets"
        filters = []
        facets = self.form.selected_facets
        for facet in facets:
            if ":" not in facet:
                continue
            field, value = facet.split(":", 1)
            field = field.replace('_', ' ').replace('exact', '').title()
            filters.append((field, value))
        return filters

    def extra_context(self):
        extra = super(FacetedSearchView, self).extra_context()
        extra['filters'] = self.clean_filters
        if self.results == []:
            extra['facets'] = self.form.search().facet_counts()
        else:
            extra['facets'] = self.results.facet_counts()
        model_type = self.request.path.split('/')[1].rstrip('s')

        extra['model_type'] = model_type
        if model_type in ['package', 'project']:
            extra['model_create'] = '%s_create' % model_type
        return extra


def search_listing(request, model_type):
    # Extract the model type from the full path, which should be the plural name
    # of a valid model type (ex: '/users/')
    model_type = model_type.rstrip('s')
    if model_type not in MODEL_FACETS.keys():
        raise Http404
    sqs = SearchQuerySet().filter(model=model_type, is_active=True)
    sqs = sqs.order_by('name')
    for facet in MODEL_FACETS[model_type]:
        sqs = sqs.facet(facet)
    view = search_view_factory(
        view_class=FacetedSearchListingView,
        template='search/search.html',
        searchqueryset=sqs,
        form_class=FacetedSearchListingForm,
    )
    return view(request)
