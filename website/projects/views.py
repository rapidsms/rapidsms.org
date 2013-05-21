from django.views.generic import TemplateView


class ProjectDetail(TemplateView):
    template_name = 'projects/detail.html'


class ProjectEdit(TemplateView):
    template_name = 'projects/edit.html'


class ProjectList(TemplateView):
    template_name = 'projects/list.html'
