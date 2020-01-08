from django.conf.urls import url
from django.contrib.auth import views, logout
from django.urls import reverse_lazy

from ..views import search_listing
from .views import Registration, UserDetail, UserEdit

urlpatterns = [
    url(r'^$', search_listing, {'model_type': 'users'}, name='user_list'),
    url(r'^(?P<pk>\d+)/$', UserDetail.as_view(), name='user_detail'),
    url(r'^(?P<pk>\d+)/edit/$', UserEdit.as_view(), name='user_edit'),

    # Log in via GitHub.
    # url(r'^login/github/$',
    #     RapidSMSOAuthRedirect.as_view(),
    #     {'provider': 'github'},
    #     name='github_login',
    # ),
    # url(r'^login/github/callback/$',
    #     RapidSMSOAuthCallback.as_view(),
    #     {'provider': 'github'},
    #     name='github_callback',
    # ),

    # Log in with email and password.
    url(r'^login/$',
        views.auth_login,
        {'template_name': 'users/login.html'},
        name='login',
    ),

    # Logout.
    url(r'^logout/$',
        views.LogoutView.as_view(),
        name='logout',
    ),

    # Account registration.
    url(r'^register/$',
        Registration.as_view(),
        name='register',
    ),

    # Password reset.
    url(r'^account/reset/$',
        views.PasswordResetView.as_view(),
        {'template_name': 'users/password/reset.html'},
        name='reset_password',
    ),
    url(r'^account/reset/done/$',
        views.PasswordResetDoneView.as_view(),
        {'template_name': 'users/password/done.html'},
    ),
    url(r'^account/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        views.PasswordResetConfirmView.as_view(),
        {'template_name': 'users/password/confirm.html'},
    ),
    url(r'^accounts/reset/complete/$',
        views.PasswordResetCompleteView.as_view(),
        {'template_name': 'users/password/complete.html'},
    ),
]
