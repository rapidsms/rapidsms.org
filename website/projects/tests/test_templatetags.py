from django.test import RequestFactory
from django.test import TestCase
from django.template import Context, Template

from ..templatetags.facet_tags import faceted_next_prev_querystring


class FacetTagsTestCase(TestCase):
    """Tests facet_tags.py"""

    def setUp(self):
        self.request_factory = RequestFactory()

    def tag_test(self, template, context, output):
        t = Template('{% load facet_tags %}' + template)
        c = Context(context)
        self.assertEqual(t.render(c).strip(), output)

    def test_remove_facet(self):
        """Case where selected_facets is wholly removed"""
        request = self.request_factory.get(
            '/page',
            data={'q': u'', 'selected_facets': u'facet:Yes'}
        )
        template = "{% remove_facet request value %}"
        context = {"request": request, "value": 'Yes'}
        output = u'<a href="?q="><i class="icon-remove-sign"></i></a>'
        self.tag_test(template, context, output)

    def test_partial_remove_facet(self):
        """Case where 1 of N selected facets is removed"""
        request = self.request_factory.get(
            '/page',
            data={'q': u'', 'selected_facets': [u'facet:Yes', u'facet1:Blue']}
        )
        template = "{% remove_facet request value %}"
        context = {"request": request, "value": 'Blue'}
        output = u'<a href="?q=&amp;selected_facets=facet%3AYes"><i class="icon-remove-sign"></i></a>'
        self.tag_test(template, context, output)

    def test_faceted_next_prev_querystring(self):
        request = self.request_factory.get(
            '/page',
            data={'q': u'', 'selected_facets': u'facet:Yes', 'page': u'1'}
        )
        page_number = 5
        qs = faceted_next_prev_querystring(request, page_number)
        self.assertIn('page=%s' % page_number, qs)
