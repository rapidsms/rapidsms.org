from django.conf.urls import patterns, url

from .views import PackageAdd, PackageDetail, PackageEdit, PackageList

urlpatterns = patterns('',
    url('^$', PackageList.as_view(), name='package_list'),
    url('^add/$', PackageAdd.as_view(), name='package_add'),
    url('^(?P<slug>[-\w]+)/$', PackageDetail.as_view(), name='package_detail'),
    url('^(?P<slug>[-\w]+)/edit/$', PackageEdit.as_view(), name='package_edit'),
)
