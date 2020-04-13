from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag('matomo.html')
def matomo():
    return {
        'site_tracker': settings.MATOMO_SITE_TRACKER,
        'site_id': str(settings.MATOMO_SITE_ID),
    }
