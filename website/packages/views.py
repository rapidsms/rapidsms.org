from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from .models import Package


class PackageDetail(DetailView):
    model = Package
    slug_field = 'slug'
    context_object_name = 'package'


class PackageAdd(CreateView):
    model = Package


class PackageEdit(UpdateView):
    model = Package
    context_object_name = 'package'


class PackageList(ListView):
    model = Package
    context_object_name = 'package_list'
    paginate_by = 10
