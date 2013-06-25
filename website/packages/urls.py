from django.conf.urls import patterns, url

from .views import PackageCreate, PackageDetail, PackageEdit, PackageFlag,\
        PackageList


urlpatterns = patterns('',
    url('^$', PackageList.as_view(), name='package_list'),
    url('^add/$', PackageCreate.as_view(), name='package_create'),
    url('^(?P<slug>[-\w]+)/$', PackageDetail.as_view(), name='package_detail'),
    url('^(?P<slug>[-\w]+)/edit/$', PackageEdit.as_view(), name='package_edit'),
    url('^(?P<slug>[-\w]+)/flag/$', PackageFlag.as_view(), name='package_flag'),
)
