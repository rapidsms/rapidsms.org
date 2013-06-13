from django.conf.urls import patterns, url

from .views import PackageCreate, PackageDelete, PackageDetail, PackageEdit,\
        PackageList


urlpatterns = patterns('',
    url('^$', PackageList.as_view(), name='package_list'),
    url('^add/$', PackageCreate.as_view(), name='package_create'),
    url('^(?P<slug>[-\w]+)/$', PackageDetail.as_view(), name='package_detail'),
    url('^(?P<slug>[-\w]+)/delete/$', PackageDelete.as_view(), name='package_delete'),
    url('^(?P<slug>[-\w]+)/edit/$', PackageEdit.as_view(), name='package_edit'),
)
