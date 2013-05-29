from django.conf.urls import patterns, url

from .views import RapidSMSOAuthRedirect, RapidSMSOAuthCallback, UserDetail, \
        UserEdit, UserList


urlpatterns = patterns('',
    url(r'^$', UserList.as_view(), name='user_list'),
    url(r'^(?P<user_id>\d+)/$', UserDetail.as_view(), name='user_detail'),
    url(r'^(?P<user_id>\d+)/edit/$', UserEdit.as_view(), name='user_edit'),

    url(r'^login/github/$',
        RapidSMSOAuthRedirect.as_view(),
        {'provider': 'github'},
        name='github-login',
    ),
    url(r'^login/github/callback/$',
        RapidSMSOAuthCallback.as_view(),
        {'provider': 'github'},
        name='github-callback',
    ),
)
