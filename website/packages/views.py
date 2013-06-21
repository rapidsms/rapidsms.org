from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import PackageCreateEditForm
from .models import Package


class PackageEditMixin(object):
    """Users may only edit and delete packages they created."""

    def get_object(self, queryset=None):
        obj = super(PackageEditMixin, self).get_object(queryset)
        if obj.creator != self.request.user:
            raise Http404()
        return obj


class PackageCreate(CreateView):
    model = Package
    form_class = PackageCreateEditForm

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(PackageCreate, self).form_valid(form)


class PackageDetail(DetailView):
    model = Package


class PackageEdit(PackageEditMixin, UpdateView):
    model = Package
    form_class = PackageCreateEditForm


class PackageList(ListView):
    model = Package
    paginate_by = 10
