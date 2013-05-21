from django.views.generic import TemplateView


class UserDetail(TemplateView):
    template_name = 'users/detail.html'


class UserEdit(TemplateView):
    template_name = 'users/edit.html'


class UserList(TemplateView):
    template_name = 'users/list.html'
