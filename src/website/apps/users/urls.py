from django.conf.urls import url
from django.contrib.auth import views

from .views import Registration, UserDetail, UserEdit, UserListView

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', UserDetail.as_view(), name='user_detail'),
    url(r'^(?P<pk>\d+)/edit/$', UserEdit.as_view(), name='user_edit'),

    url(r'^$', UserListView.as_view(), name='user_list'),
    url(r'^login/', views.LoginView.as_view(template_name='users/login.html'), name='login'),
    url(r'^logout/', views.LogoutView.as_view(), name='logout'),
    url(r'^register/$', Registration.as_view(), name='register'),

    url(r'^account/reset/$', views.PasswordResetView.as_view(), {'template_name': 'users/password/reset.html'},
        name='reset_password'),
    url(r'^account/reset/done/$', views.PasswordResetDoneView.as_view(),
        {'template_name': 'users/password/done.html'}),
    url(r'^account/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', views.PasswordResetConfirmView.as_view(),
        {'template_name': 'users/password/confirm.html'}),
    url(r'^accounts/reset/complete/$', views.PasswordResetCompleteView.as_view(),
        {'template_name': 'users/password/complete.html'}),
]
