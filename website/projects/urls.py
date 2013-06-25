from django.conf.urls import patterns, url

from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView

from ..forms import FacetedSearchListingForm

from .models import Project
from .views import ProjectCreate, ProjectDelete, ProjectDetail, ProjectEdit

# Haystack configure SQS for User Listing
sqs = SearchQuerySet()
sqs = sqs.filter(model=Project._meta.verbose_name)
facet_list = ()
for facet in facet_list:
    sqs = sqs.facet(facet)

urlpatterns = patterns('',
    url(r'^$', FacetedSearchView(form_class=FacetedSearchListingForm, searchqueryset=sqs), name='project_list'),
    url(r'^add/$', ProjectCreate.as_view(), name='project_create'),
    url(r'^d/(?P<slug>[-\w]+)/$', ProjectDetail.as_view(), name='project_detail'),
    url(r'^d/(?P<slug>[-\w]+)/delete/$', ProjectDelete.as_view(), name='project_delete'),
    url(r'^d/(?P<slug>[-\w]+)/edit/$', ProjectEdit.as_view(), name='project_edit'),
)
