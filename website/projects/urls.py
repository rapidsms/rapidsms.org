from django.conf.urls import patterns, url

from ..views import search_listing
from .views import ProjectCreate, ProjectDelete, ProjectDetail, ProjectEdit


urlpatterns = patterns('',
    url(r'^$', search_listing, {'model_type': 'projects'}, name='project_list'),
    url(r'^add/$', ProjectCreate.as_view(), name='project_create'),
    url(r'^d/(?P<slug>[-\w]+)/$', ProjectDetail.as_view(), name='project_detail'),
    url(r'^d/(?P<slug>[-\w]+)/delete/$', ProjectDelete.as_view(), name='project_delete'),
    url(r'^d/(?P<slug>[-\w]+)/edit/$', ProjectEdit.as_view(), name='project_edit'),
)
