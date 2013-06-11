import requests

from django import forms

from .models import Package


class PackageCreateEditForm(forms.ModelForm):
    pkg_type = forms.ChoiceField(label='Package Type',
            widget=forms.RadioSelect, choices=Package.PACKAGE_TYPES.items())

    class Meta:
        model = Package
        exclude = ('slug',)

    def __init__(self, *args, **kwargs):
        super(PackageCreateEditForm, self).__init__(*args, **kwargs)

        for field_name in ('has_docs', 'has_tests'):
            field = self.fields[field_name]
            field.label = field.help_text

    def clean_pypi_url(self):
        data = self.cleaned_data['pypi_url']
        if 'pypi.python.org/pypi' not in data:
            raise forms.ValidationError("The PyPI url must include "
                    "'pypi.python.org/pypi'.")
        r = requests.get(data)
        if r.status_code != '200':
            raise forms.ValidationError('Could not validate that existence of '
                    'this URL.')
        return data
