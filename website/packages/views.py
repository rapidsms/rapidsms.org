from django.views.generic import TemplateView


class PackageDetail(TemplateView):
    template_name = 'packages/detail.html'


class PackageEdit(TemplateView):
    template_name = 'packages/edit.html'


class PackageList(TemplateView):
    template_name = 'packages/list.html'
