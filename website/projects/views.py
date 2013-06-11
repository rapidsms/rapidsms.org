from django.views.generic import DetailView, ListView, CreateView, UpdateView

from .forms import ProjectCreateEditForm
from .models import Project


class ProjectCreate(CreateView):
    model = Project
    form_class = ProjectCreateEditForm


class ProjectDetail(DetailView):
    model = Project


class ProjectEdit(UpdateView):
    model = Project
    form_class = ProjectCreateEditForm


class ProjectList(ListView):
    model = Project
