from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = 'website/home.html'


class About(TemplateView):
    template_name = 'website/about.html'


class Help(TemplateView):
    template_name = 'website/help.html'


class Blogs(TemplateView):
    template_name = 'website/blogs.html'
