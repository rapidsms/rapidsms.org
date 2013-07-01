from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView,\
        UpdateView

from ..mixins import AuthorEditMixin, IsActiveMixin
from .forms import ProjectCreateEditForm
from .models import Project


class ProjectCreate(IsActiveMixin, CreateView):
    model = Project
    form_class = ProjectCreateEditForm

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(ProjectCreate, self).form_valid(form)


class ProjectDelete(IsActiveMixin, AuthorEditMixin, DeleteView):
    model = Project
    http_method_names = ('delete', 'post')
    success_url = reverse_lazy('project_list')


class ProjectDetail(IsActiveMixin, DetailView):
    model = Project


class ProjectEdit(IsActiveMixin, AuthorEditMixin, UpdateView):
    model = Project
    form_class = ProjectCreateEditForm
