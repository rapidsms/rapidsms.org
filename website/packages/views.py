from django.http import Http404
from django.views.generic import DetailView, ListView, CreateView, UpdateView

from .forms import PackageCreateEditForm
from .models import Package


class PackageCreate(CreateView):
    model = Package
    form_class = PackageCreateEditForm

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(PackageCreate, self).form_valid(form)


class PackageDetail(DetailView):
    model = Package


class PackageEdit(UpdateView):
    model = Package
    form_class = PackageCreateEditForm

    def get_object(self, queryset=None):
        obj = super(PackageEdit, self).get_object(queryset)
        if obj.creator != self.request.user:
            raise Http404()
        return obj


class PackageList(ListView):
    model = Package
    paginate_by = 10
