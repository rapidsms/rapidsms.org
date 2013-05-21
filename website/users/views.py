from django.views.generic import TemplateView


class UserList(TemplateView):
    template_name = 'users/list.html'


class UserDetail(TemplateView):
    template_name = 'users/detail.html'
