from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView,\
        UpdateView

from ..mixins import AuthorEditMixin, IsActiveObjectMixin, LoginRequiredMixin
from .forms import ProjectCreateEditForm
from .models import Project


class ProjectCreate(LoginRequiredMixin, IsActiveObjectMixin, CreateView):
    model = Project
    form_class = ProjectCreateEditForm

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(ProjectCreate, self).form_valid(form)


class ProjectDelete(LoginRequiredMixin, IsActiveObjectMixin, AuthorEditMixin,
        DeleteView):
    model = Project
    http_method_names = ('delete', 'post')
    success_url = reverse_lazy('project_list')


class ProjectDetail(IsActiveObjectMixin, DetailView):
    model = Project


class ProjectEdit(LoginRequiredMixin, IsActiveObjectMixin, AuthorEditMixin,
        UpdateView):
    model = Project
    form_class = ProjectCreateEditForm
