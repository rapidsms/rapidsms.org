from django.views.generic import DetailView, ListView, CreateView, UpdateView

from .forms import PackageForm
from .models import Package


class PackageDetail(DetailView):
    model = Package
    slug_field = 'slug'


class PackageAdd(CreateView):
    model = Package
    form_class = PackageForm


class PackageEdit(UpdateView):
    model = Package
    form_class = PackageForm


class PackageList(ListView):
    model = Package
    paginate_by = 10
