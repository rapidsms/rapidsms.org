from django.conf.urls import patterns, url

from ..views import search_listing
from .views import ProjectCreate, ProjectDelete, ProjectDetail, ProjectEdit
from .views import ProjectReviewRequest, ProjectReviewList, ProjectApprove


urlpatterns = patterns('',
    url(r'^$', search_listing, {'model_type': 'projects'},
        name='project_list'),
    url(r'^add/$', ProjectCreate.as_view(),
        name='project_create'),
    url(r'^need-review/$', ProjectReviewList.as_view(),
        name='projects_project_reviews'),
    url(r'^(?P<slug>[-\w]+)/$', ProjectDetail.as_view(),
        name='project_detail'),
    url(r'^(?P<slug>[-\w]+)/delete/$', ProjectDelete.as_view(),
        name='project_delete'),
    url(r'^(?P<slug>[-\w]+)/edit/$', ProjectEdit.as_view(),
        name='project_edit'),
    url(r'^(?P<slug>[-\w]+)/publish/$', ProjectApprove.as_view(),
        name='project_publish'),
    url(r'^(?P<slug>[-\w]+)/review-request/$', ProjectReviewRequest.as_view(),
        name='project_review_request'),
)
