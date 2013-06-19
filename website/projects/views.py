from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.views.generic import CreateView, DeleteView, DetailView, ListView,\
        UpdateView

from .forms import ProjectCreateEditForm
from .models import Project


class ProjectEditMixin(object):
    """Users may only edit and delete projects they created."""

    def get_object(self, queryset=None):
        obj = super(ProjectEditMixin, self).get_object(queryset)
        if obj.creator != self.request.user:
            raise Http404()
        return obj


class ProjectCreate(CreateView):
    model = Project
    form_class = ProjectCreateEditForm

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(ProjectCreate, self).form_valid(form)


class ProjectDelete(ProjectEditMixin, DeleteView):
    model = Project
    http_method_names = ('delete', 'post')
    success_url = reverse_lazy('project_list')


class ProjectDetail(DetailView):
    model = Project


class ProjectEdit(ProjectEditMixin, UpdateView):
    model = Project
    form_class = ProjectCreateEditForm


class ProjectList(ListView):
    model = Project
