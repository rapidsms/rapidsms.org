import json
import random

from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView,\
    UpdateView, RedirectView
from django.views.generic.detail import SingleObjectMixin

from ..mixins import LoginRequiredMixin, CanEditMixin
from .forms import ProjectCreateEditForm
from .models import Project


class ProjectCreate(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectCreateEditForm

    def form_valid(self, form):
        form.instance.creator = self.request.user
        ret_val = super(ProjectCreate, self).form_valid(form)
        self.object.collaborators.add(self.request.user)
        return ret_val


class ProjectDelete(LoginRequiredMixin, CanEditMixin,
        DeleteView):
    model = Project
    http_method_names = ('delete', 'post')
    success_url = reverse_lazy('project_list')


class ProjectDetail(DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        project = context['object']
        map_data = {}
        countries = project.countries.all()
        for country in countries:
            scope = country.scope
            map_data[country.code] = project.get_map_data(country)
        context.update({
            'map_data': json.dumps(map_data),
            'scope': json.dumps(scope.json_serializable()),
        })
        return context


class ProjectEdit(LoginRequiredMixin, CanEditMixin,
        UpdateView):
    model = Project
    form_class = ProjectCreateEditForm


class ProjectReviewRequest(LoginRequiredMixin, CanEditMixin,
        SingleObjectMixin, RedirectView):
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
        project.change_status('R', send_notification=True)  # Status saved.
        messages.success(self.request, 'We have notified the administrators'
            ' and they will review this request shortly')
        return super(ProjectReviewRequest, self).get(self, self.request, *args,
            **kwargs)
