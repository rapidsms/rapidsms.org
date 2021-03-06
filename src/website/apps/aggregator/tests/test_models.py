# email test
# https://docs.djangoproject.com/en/dev/topics/testing/#email-services
import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from django_push.subscriber.models import SubscriptionManager
from mock import patch

from .. import models
from ..management.commands import send_pending_approval_email
from .base import MockResponse


class AggregatorTests(TestCase):

    def setUp(self):
        Group.objects.all().delete()
        settings.SUPERFEEDR_CREDS = True
        with patch.object(SubscriptionManager, 'subscribe', return_value=MockResponse('fake')):
            # Set up users who will get emailed
            g = Group.objects.create(name=settings.FEED_APPROVERS_GROUP_NAME)
            self.user = get_user_model().objects.create(name="Mr. Potato", email="mr@potato.com")
            self.user.groups.add(g)

            self.feed_type = models.FeedType(
                name="Test Feed Type",
                slug="test-feed-type",
                can_self_add=True)
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
                feed_item = models.FeedItem(
                    feed=feed,
                    title="%s Item" % feed.title, link=feed.public_url,
                    date_modified=datetime.datetime.now(), guid=feed.title)
                feed_item.save()
                self.assertEqual(feed.__str__(), feed.title)

            self.client = Client()

    def test_feed_list_only_approved_and_active(self):
        response = self.client.get(reverse('community-feed-list', kwargs={'feed_type_slug': self.feed_type.slug}))
        for item in response.context['object_list']:
            self.assertEqual(models.APPROVED_FEED, item.feed.approval_status)

    def test_management_command_sends_no_email_with_no_pending_feeds(self):
        self.pending_feed.delete()
        send_pending_approval_email.Command().handle_noargs()
        self.assertEqual(0, len(mail.outbox))

    def test_management_command_sends_email_with_pending_feeds(self):
        send_pending_approval_email.Command().handle_noargs()
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual(mail.outbox[0].to, [self.user.email])
