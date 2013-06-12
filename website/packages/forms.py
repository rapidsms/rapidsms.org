import requests

from django import forms

from .models import Package


class PackageCreateEditForm(forms.ModelForm):
    pkg_type = forms.ChoiceField(label='Package Type',
            widget=forms.RadioSelect, choices=Package.PACKAGE_TYPES.items())

    class Meta:
        model = Package
        fields = ('name', 'pkg_type', 'description', 'pypi_url',
                'repository_url', 'has_tests', 'has_docs')

    def clean_pypi_url(self):
        data = self.cleaned_data['pypi_url']
        if 'pypi.python.org/pypi' not in data:
            raise forms.ValidationError("The PyPI url must include "
                    "'pypi.python.org/pypi'.")
        r = requests.get(data)
        if r.status_code != 200:
            raise forms.ValidationError('Could not validate that existence of '
                    'this URL.')
        return data
