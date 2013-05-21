from django.conf.urls import patterns, url

from website.projects.views import ProjectDetail, ProjectEdit, ProjectList


urlpatterns = patterns('',
    url(r'^$', ProjectList.as_view(), name='project_list'),
    url(r'^(?P<project_id>\d+)/$', ProjectDetail.as_view(), name='project_detail'),
    url(r'^(?P<project_id>\d+)/edit/$', ProjectEdit.as_view(), name='project_edit'),
)
