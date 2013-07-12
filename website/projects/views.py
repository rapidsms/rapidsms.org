from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView,\
    UpdateView, RedirectView
from django.views.generic.detail import SingleObjectMixin

from ..mixins import AuthorEditMixin, IsActiveObjectMixin, LoginRequiredMixin
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


class ProjectReviewRequest(LoginRequiredMixin, IsActiveObjectMixin,
        AuthorEditMixin, SingleObjectMixin, RedirectView):
    http_method_names = ['post', ]
    model = Project

    def get_redirect_url(self, *args, **kargs):
        """ Return absolute url for current instance """
        project = self.get_object()
        url = project.get_absolute_url()
        return url

    def post(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        project = self.get_object()
        project.change_status('R', send_notification=True)  # Status saved.
        messages.success(self.request, 'We have notified the administrators'
            ' and they will review this request shortly')
        return super(ProjectReviewRequest, self).get(self, self.request, *args,
            **kwargs)
