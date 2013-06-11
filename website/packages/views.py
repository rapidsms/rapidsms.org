from django.views.generic import DetailView, ListView, CreateView, UpdateView

from .forms import PackageCreateEditForm
from .models import Package


class PackageCreate(CreateView):
    model = Package
    form_class = PackageCreateEditForm


class PackageDetail(DetailView):
    model = Package


class PackageEdit(UpdateView):
    model = Package
    form_class = PackageCreateEditForm


class PackageList(ListView):
    model = Package
    paginate_by = 10
