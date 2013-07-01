from itertools import chain
import os

from django.conf import settings
from django.http import Http404
from django.views.generic import TemplateView

from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView, search_view_factory

from .forms import FacetedSearchListingForm


MODEL_FACETS = {
    'package': ('pkg_type', ),
    'project': ('countries', 'creator'),
    'user': ('countries', 'for_hire', ),
}


class Home(TemplateView):
    template_name = 'website/home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context.update({
            'RAPIDSMS_VERSION': getattr(settings, 'RAPIDSMS_VERSION'),
        })
        return context


class About(TemplateView):
    template_name = 'website/about.html'


class Help(TemplateView):
    template_name = 'website/help.html'


class Blogs(TemplateView):
    template_name = 'website/blogs.html'


class FacetedSearchListingView(FacetedSearchView):

    def extra_context(self):
        extra = super(FacetedSearchView, self).extra_context()
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
    sqs = SearchQuerySet().filter(model=model_type)
    for facet in MODEL_FACETS[model_type]:
        sqs = sqs.facet(facet)
    view = search_view_factory(
        view_class=FacetedSearchListingView,
        template='search/search.html',
        searchqueryset=sqs,
        form_class=FacetedSearchListingForm,
    )
    return view(request)
