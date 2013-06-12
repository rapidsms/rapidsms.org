from django.http import Http404
from django.views.generic import DetailView, ListView, CreateView, UpdateView

from .forms import ProjectCreateEditForm
from .models import Project


class ProjectCreate(CreateView):
    model = Project
    form_class = ProjectCreateEditForm

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(ProjectCreate, self).form_valid(form)


class ProjectDetail(DetailView):
    model = Project


class ProjectEdit(UpdateView):
    model = Project
    form_class = ProjectCreateEditForm

    def get_object(self, queryset=None):
        obj = super(ProjectEdit, self).get_object(queryset)
        if obj.creator != self.request.user:
            raise Http404()
        return obj


class ProjectList(ListView):
    model = Project
