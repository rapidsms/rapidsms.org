from django.views.generic import DetailView, ListView, CreateView, UpdateView

from .models import Project


class ProjectCreate(CreateView):
    model = Project


class ProjectDetail(DetailView):
    model = Project


class ProjectEdit(UpdateView):
    model = Project


class ProjectList(ListView):
    model = Project
