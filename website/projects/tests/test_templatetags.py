from django.test import RequestFactory
from django.test import TestCase

from ..templatetags.facet_tags import faceted_next_prev_querystring
from ..templatetags.facet_tags import remove_facet


class FacetTagsTestCase(TestCase):
    """Tests facet_tags.py"""

    def setUp(self):
        self.request_factory = RequestFactory()

    def test_remove_facet(self):
        """Case where selected_facets is wholly removed"""
        request = self.request_factory.get(
            '/page',
            data={'q': u'', 'selected_facets': u'facet:Yes'}
        )
        facet_value = 'Yes'
        qs = remove_facet(request, facet_value)
        self.assertNotIn('selected_facets=facet%3A:{0}'.format(facet_value), qs)

    def test_partial_remove_facet(self):
        """Case where 1 of N selected facets is removed"""
        request = self.request_factory.get(
            '/page',
            data={'q': u'', 'selected_facets': [u'facet:Yes', u'facet1:Blue']}
        )
        removed_facet_value = 'Yes'
        retained_facet_value = 'Blue'
        qs = remove_facet(request, removed_facet_value)
        self.assertNotIn('selected_facets=facet%3A:{0}'.format(removed_facet_value), qs)
        self.assertIn('selected_facets=facet1%3A{0}'.format(retained_facet_value), qs)

    def test_faceted_next_prev_querystring(self):
        request = self.request_factory.get(
            '/page',
            data={'q': u'', 'selected_facets': u'facet:Yes', 'page': u'1'}
        )
        page_number = 5
        qs = faceted_next_prev_querystring(request, page_number)
        self.assertIn('page={0}'.format(page_number), qs)
