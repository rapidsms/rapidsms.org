from django.conf.urls import patterns, url

from .views import ProjectCreate, ProjectDetail, ProjectEdit, ProjectList


urlpatterns = patterns('',
    url(r'^$', ProjectList.as_view(), name='project_list'),
    url(r'^add/$', ProjectCreate.as_view(), name='project_create'),
    url(r'^(?P<slug>[-\w]+)/$', ProjectDetail.as_view(), name='project_detail'),
    url(r'^(?P<slug>[-\w]+)/edit/$', ProjectEdit.as_view(), name='project_edit'),
)
