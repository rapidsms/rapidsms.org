from django.conf import settings
from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = 'website/home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context.update({
            'RAPIDSMS_VERSION': getattr(settings, 'RAPIDSMS_VERSION'),
        })
        return context


class About(TemplateView):
    template_name = 'website/about.html'


class Help(TemplateView):
    template_name = 'website/help.html'


class Blogs(TemplateView):
    template_name = 'website/blogs.html'

