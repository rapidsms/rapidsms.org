from django import template

from urllib import urlencode

register = template.Library()


@register.inclusion_tag('includes/remove_facet.html')
def remove_facet(request, facet_value):
    """"Returns a template that provides the URL required to remove
        the current facet from the querystring

        Example:
            {% load facet_tags %}
            {% remove_facet request value %}

        Renders:
            <a href="{{ remove_facet_querystring }}"><i class="icon-remove-sign"></i></a>
    """
    params = {}
    for param in request.GET.lists():
        # reconstruct the non-selected_facets params
        if param[0] != 'selected_facets':
            for v in param[1]:
                params[param[0]] = v
        else:
            for v in param[1]:
                # exclude the selected_facet param that matches the supplied
                # facet_value
                if facet_value != v.split(':')[1]:
                    params[param[0]] = v
    querystring = '?%s' % urlencode(params)
    return {"remove_facet_querystring": querystring}
