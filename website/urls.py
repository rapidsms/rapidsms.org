from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet

from .aggregator.feeds import CommunityAggregatorFeed, CommunityAggregatorFirehoseFeed

from .views import About, Community, FacetedSearchCustomView, Help, Home, Ecosystem


admin.autodiscover()


urlpatterns = [
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += [
    url(r'^scribbler/', include('scribbler.urls')),
    url(r'^selectable/', include('selectable.urls')),
]

urlpatterns += [
    url(r'^$', Home.as_view(), name='home'),
    url(r'^about/$', About.as_view(), name='about'),
    url(r'^community/$', Community.as_view(), name='community'),
    url(r'^help/$', Help.as_view(), name='help'),
    url(r'^ecosystem/$', Ecosystem.as_view(), name='ecosystem'),

    url(r'^projects/', include('website.projects.urls')),
    url(r'^packages/', include('website.packages.urls')),
    url(r'^users/', include('website.users.urls')),

    url(r'^blogs/', include('website.aggregator.urls')),
    url(r'^rss/community/blogs/firehose/$', CommunityAggregatorFirehoseFeed(), name='aggregator-firehose-feed'),
    url(r'^rss/community/blogs/(?P<slug>[\w-]+)/$', CommunityAggregatorFeed(), name='aggregator-feed'),
    # django-push
    url(r'^subscriber/', include('django_push.subscriber.urls')),
]


# Haystack configure SQS for faceting
sqs = SearchQuerySet()
facet_list = ('countries', 'creator', 'pkg_type', 'model', 'user_type',
    'taxonomy', 'num_users', 'collaborators', 'license')
for facet in facet_list:
    sqs = sqs.facet(facet)

urlpatterns += [
    url(r'^search/$',
        FacetedSearchCustomView(form_class=FacetedSearchForm, searchqueryset=sqs),
        name='haystack_search',
    ),
]
