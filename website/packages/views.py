from django.views.generic import TemplateView


class PackageList(TemplateView):
    template_name = 'packages/list.html'


class PackageDetail(TemplateView):
    template_name = 'package/detail.html'
