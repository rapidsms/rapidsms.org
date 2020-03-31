import json

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, RedirectView, UpdateView
from django.views.generic.detail import SingleObjectMixin

from website.apps.core.mixins import CanEditMixin, LoginRequiredMixin, StaffRequiredMixin
from website.apps.core.views import RapidSMSListView

from .forms import ProjectCreateEditForm
from .models import Project


class ProjectCreate(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectCreateEditForm

    def form_valid(self, form):
        form.instance.creator = self.request.user
        ret_val = super().form_valid(form)
        self.object.collaborators.add(self.request.user)
        return ret_val


class ProjectDelete(LoginRequiredMixin, CanEditMixin, DeleteView):
    model = Project
    http_method_names = ('delete', 'post')
    success_url = reverse_lazy('project_list')


class ProjectDetail(DetailView):
    model = Project

    @staticmethod
    def get_map_data(project, countries):
        scope = countries[0].scope
        map_data = {country.code: project.get_map_data(country)
                    for country in countries}
        data = {
            'map_data': json.dumps(map_data),
            'scope': json.dumps(scope.json_serializable()),
        }
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = context['object']
        countries = project.countries.all()
        if countries:
            map_data = self.get_map_data(project, countries)
            context.update(map_data)
        return context


class ProjectReviewList(StaffRequiredMixin, ListView):
    model = Project

    def get_queryset(self):
        projects = super().get_queryset()
        return projects.filter(status=Project.NEEDS_REVIEW)


class ProjectApprove(StaffRequiredMixin, UpdateView):
    model = Project

    def post(self, request, *args, **kwargs):
        object = self.get_object()
        object.change_status(status=Project.PUBLISHED)
        messages.success(self.request, 'Project has been successfully published.')
        return redirect(object)


class ProjectEdit(LoginRequiredMixin, CanEditMixin, UpdateView):
    model = Project
    form_class = ProjectCreateEditForm


class ProjectReviewRequest(LoginRequiredMixin, CanEditMixin, SingleObjectMixin,
                           RedirectView):
    http_method_names = ['post', ]
    model = Project

    def get_redirect_url(self, *args, **kargs):
        """ Return absolute url for current instance """
        project = self.get_object()
        url = project.get_absolute_url()
        return url

    def post(self, request, *args, **kwargs):
        """Updates project status to 'needs revision'"""
        project = self.get_object()
        project.change_status('R')  # Project saved and status changed.
        messages.success(self.request, 'We have notified the administrators and they will review this request shortly')
        return super().get(self, self.request, *args, **kwargs)


class ProjectListView(RapidSMSListView):
    model = Project
