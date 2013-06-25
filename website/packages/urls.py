from django.conf.urls import patterns, url

from .views import PackageCreate, PackageDetail, PackageEdit, PackageFlag,\
        PackageRefresh

urlpatterns = patterns('',
    url(r'^$', 'website.views.search_listing', name='package_list'),
    url(r'^add/$', PackageCreate.as_view(), name='package_create'),
    url(r'^d/(?P<slug>[-\w]+)/$', PackageDetail.as_view(), name='package_detail'),
    url(r'^d/(?P<slug>[-\w]+)/edit/$', PackageEdit.as_view(), name='package_edit'),
    url(r'^d/(?P<slug>[-\w]+)/flag/$', PackageFlag.as_view(), name='package_flag'),
    url(r'^d/(?P<slug>[-\w]+)/refresh/$', PackageRefresh.as_view(), name='package_refresh'),
)
