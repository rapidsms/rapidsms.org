from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy

from ..views import search_listing
from .views import RapidSMSOAuthRedirect, RapidSMSOAuthCallback, Registration,\
        UserDetail, UserEdit


urlpatterns = patterns('',
    url(r'^$', search_listing, {'model_type': 'users'}, name='user_list'),
    url(r'^d/(?P<pk>\d+)/$', UserDetail.as_view(), name='user_detail'),
    url(r'^d/(?P<pk>\d+)/edit/$', UserEdit.as_view(), name='user_edit'),

    # Log in via GitHub.
    url(r'^login/github/$',
        RapidSMSOAuthRedirect.as_view(),
        {'provider': 'github'},
        name='github_login',
    ),
    url(r'^login/github/callback/$',
        RapidSMSOAuthCallback.as_view(),
        {'provider': 'github'},
        name='github_callback',
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

    # Password reset.
    url(r'^account/reset/$',
       'django.contrib.auth.views.password_reset',
        {'template_name': 'users/password/reset.html'},
        name='reset_password',
    ),
    url(r'^account/reset/done/$',
        'django.contrib.auth.views.password_reset_done',
        {'template_name': 'users/password/done.html'},
    ),
    url(r'^account/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'template_name': 'users/password/confirm.html'},
    ),
    url(r'^accounts/reset/complete/$',
        'django.contrib.auth.views.password_reset_complete',
        {'template_name': 'users/password/complete.html'},
    ),
)
