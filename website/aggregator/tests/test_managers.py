from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.test import TestCase
from mock import patch
from django_push.subscriber.models import SubscriptionManager

from .base import MockResponse
from ..models import FeedItem
from .. import models

__all__ = ['FeedItemManagerTest', ]


class FeedItemManagerTest(TestCase):

    def setUp(self):
        Group.objects.all().delete()
        settings.SUPERFEEDR_CREDS = True
        with patch.object(SubscriptionManager, 'subscribe',
                return_value=MockResponse('fake')):
            # Set up users who will get emailed
            g = Group.objects.create(name=settings.FEED_APPROVERS_GROUP_NAME)
            self.user = get_user_model().objects.create(name="Mr. Potato",
                email="mr@potato.com")
            self.user.groups.add(g)

            self.feed_type = models.FeedType(name="Test Feed Type",
                slug="test-feed-type", can_self_add=True)
            self.feed_type.save()

            self.approved_feed = models.Feed(
                title="Approved",
                feed_url="foo.com/rss/",
                public_url="foo.com/",
                is_defunct=False,
                approval_status=models.APPROVED_FEED,
                feed_type=self.feed_type
            )
            self.denied_feed = models.Feed(
                title="Denied",
                feed_url="bar.com/rss/",
                public_url="bar.com/",
                is_defunct=False,
                approval_status=models.DENIED_FEED,
                feed_type=self.feed_type
            )
            self.pending_feed = models.Feed(
                title="Pending",
                feed_url="baz.com/rss/",
                public_url="baz.com/",
                is_defunct=False,
                approval_status=models.PENDING_FEED,
                feed_type=self.feed_type
            )
            self.defunct_feed = models.Feed(
                title="Defunct",
                feed_url="zot.com/rss/",
                public_url="zot.com/",
                is_defunct=True,
                approval_status=models.APPROVED_FEED,
                feed_type=self.feed_type
            )

            feeds = [
                self.approved_feed, self.denied_feed, self.pending_feed,
                self.defunct_feed
            ]
            for feed in feeds:
                feed.save()

    def test_create_or_update_by_guid_item_doesnt_exists(self):
        kwargs = {"feed_id": self.approved_feed.id}
        items = FeedItem.objects.all()
        self.failIf(items.count())
        item = FeedItem.objects.create_or_update_by_guid("abc", **kwargs)
        items = FeedItem.objects.all()
        self.assertEqual(items.count(), 1)