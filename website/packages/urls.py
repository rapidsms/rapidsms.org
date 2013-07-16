from django.conf.urls import patterns, url

from ..views import search_listing
from .views import PackageCreate, PackageDetail, PackageEdit, PackageFlag,\
        PackageRefresh

urlpatterns = patterns('',
    url(r'^$', search_listing, {'model_type': 'packages'}, name='package_list'),
    url(r'^add/$', PackageCreate.as_view(), name='package_create'),
    url(r'^(?P<slug>[-\w]+)/$', PackageDetail.as_view(), name='package_detail'),
    url(r'^(?P<slug>[-\w]+)/edit/$', PackageEdit.as_view(), name='package_edit'),
    url(r'^(?P<slug>[-\w]+)/flag/$', PackageFlag.as_view(), name='package_flag'),
    url(r'^(?P<slug>[-\w]+)/refresh/$', PackageRefresh.as_view(), name='package_refresh'),
)
