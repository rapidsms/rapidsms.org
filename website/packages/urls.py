from django.conf.urls import patterns, url

from website.packages.views import PackageDetail, PackageList

urlpatterns = patterns('',
    url('^$', PackageList.as_view(), name='package_list'),
    url('^(?P<package_id>\d+)/$', PackageDetail.as_view(), name='package_detail'),
)
