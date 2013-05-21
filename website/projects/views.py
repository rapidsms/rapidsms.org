from django.views.generic import TemplateView


class ProjectList(TemplateView):
    template_name = 'projects/list.html'


class ProjectDetail(TemplateView):
    template_name = 'projects/detail.html'
