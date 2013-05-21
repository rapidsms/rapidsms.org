from django.conf.urls import patterns, url

from website.users.views import UserDetail, UserEdit, UserList


urlpatterns = patterns('',
    url(r'^$', UserList.as_view(), name='user_list'),
    url(r'^(?P<user_id>\d+)/$', UserDetail.as_view(), name='user_detail'),
    url(r'^(?P<user_id>\d+)/edit/$', UserEdit.as_view(), name='user_edit'),
)
