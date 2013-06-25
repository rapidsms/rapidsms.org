from django.conf.urls import patterns, url

from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView

from ..forms import FacetedSearchListingForm

from .models import Package
from .views import PackageCreate, PackageDetail, PackageEdit, PackageFlag,\
        PackageRefresh

# Haystack configure SQS for User Listing
sqs = SearchQuerySet()
sqs = sqs.filter(model=Package._meta.verbose_name)
facet_list = ()
for facet in facet_list:
    sqs = sqs.facet(facet)

urlpatterns = patterns('',
    url(r'^$', FacetedSearchView(form_class=FacetedSearchListingForm, searchqueryset=sqs), name='package_list'),
    url(r'^add/$', PackageCreate.as_view(), name='package_create'),
    url(r'^d/(?P<slug>[-\w]+)/$', PackageDetail.as_view(), name='package_detail'),
    url(r'^d/(?P<slug>[-\w]+)/edit/$', PackageEdit.as_view(), name='package_edit'),
    url(r'^d/(?P<slug>[-\w]+)/flag/$', PackageFlag.as_view(), name='package_flag'),
    url(r'^d/(?P<slug>[-\w]+)/refresh/$', PackageRefresh.as_view(), name='package_refresh'),
)
