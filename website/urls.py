from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView

from .views import About, Blogs, Help, Home


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += patterns('',
    url(r'^scribbler/', include('scribbler.urls')),
    url(r'^selectable/', include('selectable.urls')),
)

urlpatterns += patterns('',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^about/$', About.as_view(), name='about'),
    url(r'^blogs/$', Blogs.as_view(), name='blogs'),
    url(r'^help/$', Help.as_view(), name='help'),

    url(r'^projects/', include('website.projects.urls')),
    url(r'^packages/', include('website.packages.urls')),
    url(r'^users/', include('website.users.urls')),
)

# Haystack configure SQS for faceting
sqs = SearchQuerySet()
facet_list = ('countries', 'creator', 'pkg_type', 'model', 'user_type',
    'taxonomy')
for facet in facet_list:
    sqs = sqs.facet(facet)

urlpatterns += patterns('haystack.views',
    url(r'^search/$',
        FacetedSearchView(form_class=FacetedSearchForm, searchqueryset=sqs),
        name='haystack_search',
    ),
)
