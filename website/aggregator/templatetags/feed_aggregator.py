from __future__ import absolute_import

from django import template
from ..models import Feed, FeedItem

register = template.Library()


class FeedListNode(template.Node):
    def __init__(self, varname):
        self.varname = varname

    def render(self, context):
        context[self.varname] = Feed.objects.filter(is_defunct=False)
        return ''

def do_get_feed_list(parser, token):
    """
    {% get_feed_list as feed_list %}
    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError, "'%s' tag takes two arguments" % bits[0]
    if bits[1] != "as":
        raise template.TemplateSyntaxError, "First argument to '%s' tag must be 'as'" % bits[0]
    return FeedListNode(bits[2])


@register.assignment_tag
def get_latest_feeditems():
    """Returns a list of the latest 10 feed items """
    items = FeedItem.objects.all()
    num_items = items.count()
    if num_items > 10:
        return items[:10]
    return items

register.tag('get_feed_list', do_get_feed_list)
