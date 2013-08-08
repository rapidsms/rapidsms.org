import json
import random

from datamaps.models import Scope
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from django.shortcuts import redirect, render_to_response
from django.views.generic import TemplateView
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView, search_view_factory

from website.projects.models import Project
from .forms import FacetedSearchListingForm


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
        context = super(Home, self).get_context_data(**kwargs)
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


class FacetedSearchCustomView(FacetedSearchView):
    """Overrides various default methods to allow for additional context, smoother
       UX for faceting
    """

    def build_page(self):
        """
        Paginates the results appropriately.

        Overriden to redirect to page 1 if a page_no is not found
        """
        try:
            page_no = int(self.request.GET.get('page', 1))
        except (TypeError, ValueError):
            raise Http404("Not a valid number for page.")

        if page_no < 1:
            raise Http404("Pages should be 1 or greater.")

        paginator = Paginator(self.results, self.results_per_page)
        # import pdb; pdb.set_trace()
        try:
            page = paginator.page(page_no)
        except InvalidPage:
            # Redirect to page 1 of the
            path = self.request.path
            qs = self.request.GET.copy()
            qs['page'] = 1
            url = '%s?%s' % (path, qs.urlencode())
            return redirect(url)

        return paginator, page

    def clean_filters(self):
        """Returns a list of tuples (filter, value) of applied facets"""
        filters = []
        # get distinct facets
        facets = list(set(self.form.selected_facets))
        for facet in facets:
            if ":" not in facet:
                continue
            field, value = facet.split(":", 1)
            field = field.replace('_', ' ').replace('exact', '').title()
            filters.append((field, value))
        return filters

    def create_response(self):
        """
        Generates the actual HttpResponse to send back to the user.

        Overriding to allow the redirect to pass through from overriden build_page
        """
        try:
            (paginator, page) = self.build_page()
        except ValueError:
            return self.build_page()

        context = {
            'query': self.query,
            'form': self.form,
            'page': page,
            'paginator': paginator,
            'suggestion': None,
        }

        if self.results and hasattr(self.results, 'query') and self.results.query.backend.include_spelling:
            context['suggestion'] = self.form.get_suggestion()

        context.update(self.extra_context())
        return render_to_response(self.template, context, context_instance=self.context_class(self.request))

    def extra_context(self):
        extra = super(FacetedSearchCustomView, self).extra_context()
        extra['filters'] = self.clean_filters()
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
    sqs = sqs.order_by('name')
    for facet in MODEL_FACETS[model_type]:
        sqs = sqs.facet(facet)
    view = search_view_factory(
        view_class=FacetedSearchCustomView,
        template='search/search.html',
        searchqueryset=sqs,
        form_class=FacetedSearchListingForm,
    )
    return view(request)
