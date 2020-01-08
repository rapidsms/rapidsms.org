from __future__ import absolute_import

from django.urls import reverse
from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from .models import FeedType, FeedItem


class BaseCommunityAggregatorFeed(Feed):
    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.summary

    def item_guid(self, item):
        return item.guid

    def item_link(self, item):
        return item.link

    def item_author_name(self, item):
        return item.feed.title

    def item_author_link(self, item):
        return item.feed.public_url

    def item_pubdate(self, item):
        return item.date_modified


class CommunityAggregatorFeed(BaseCommunityAggregatorFeed):
    def get_object(self, request, slug=None):
        return get_object_or_404(FeedType, slug=slug)

    def items(self, obj):
        qs = FeedItem.objects.filter(feed__feed_type=obj)
        qs = qs.order_by('-date_modified')
        qs = qs.select_related('feed', 'feed__feed_type')
        return qs[:25]

    def title(self, obj):
        return "Community aggregator: %s" % obj.name

    def link(self, obj):
        return urlresolvers.reverse('aggregator-feed', args=[obj.slug])

    def description(self, obj):
        return self.title(obj)


class CommunityAggregatorFirehoseFeed(BaseCommunityAggregatorFeed):
    title = 'RapidSMS community aggregator firehose'
    description = 'All activity from the RapidSMS community aggregator'

    def link(self):
        return reverse('aggregator-firehose-feed')

    def items(self):
        qs = FeedItem.objects.order_by('-date_modified').select_related('feed')
        return qs[:50]
