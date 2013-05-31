from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy

from .views import RapidSMSOAuthRedirect, RapidSMSOAuthCallback, Registration,\
        UserDetail, UserEdit, UserList


urlpatterns = patterns('',
    url(r'^$', UserList.as_view(), name='user_list'),
    url(r'^(?P<user_id>\d+)/$', UserDetail.as_view(), name='user_detail'),
    url(r'^(?P<user_id>\d+)/edit/$', UserEdit.as_view(), name='user_edit'),

    # Log in via Github.
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

    # Log in with email and password.
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'users/login.html'},
        name='login',
    ),

    # Logout.
    url(r'^logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': reverse_lazy('home')},
        name='logout',
    ),

    # Account registration.
    url(r'^register/$',
        Registration.as_view(),
        name='register',
    ),
)
