from django import template
from hashlib import md5


register = template.Library()


@register.simple_tag
def gravatar_url(email, size=32):
    """
    Return the full URL for a Gravatar given an email hash.
    """
    bits = md5(email.lower().encode('utf-8')).hexdigest()
    return "https://secure.gravatar.com/avatar/%s?s=%s" % (bits, size)
