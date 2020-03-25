from django.conf.urls import url

from .views import (
    ProjectApprove,
    ProjectCreate,
    ProjectDelete,
    ProjectDetail,
    ProjectEdit,
    ProjectListView,
    ProjectReviewList,
    ProjectReviewRequest,
)

urlpatterns = [
    url(r'^$', ProjectListView.as_view(), name='project_list'),
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
]
