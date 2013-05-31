import requests

from django import forms

from .models import Package


class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        exclude = ('slug',)

    def clean_pypi_url(self):
        data = self.cleaned_data['pypi_url']
        if 'pypi.python.org/pypi' not in data:
            raise forms.ValidationError("The pypi url must include pypi.python.org/pypi")
        r = requests.get(data)
        if r.status_code != '200':
            raise forms.ValidationError("Could not validate that existence of the URL")
        return data
