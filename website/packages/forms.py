import requests

from django import forms

from .models import Package


class PackageCreateEditForm(forms.ModelForm):
    pkg_type = forms.ChoiceField(label='Package Type',
            widget=forms.RadioSelect, choices=Package.PACKAGE_TYPES.items())

    class Meta:
        model = Package
        fields = ('pkg_type', 'name', 'docs_url', 'tests_url', 'repo_url',
                'home_url')

    def __init__(self, *args, **kwargs):
        super(PackageCreateEditForm, self).__init__(*args, **kwargs)

        # Package type and name are not editable once the project has been
        # created.
        if self.instance.pk:
            self.fields.pop('pkg_type')
            self.fields.pop('name')

    def clean_name(self):
        name = self.cleaned_data['name']
        self.instance.name = name
        r = requests.get(self.instance.get_pypi_json_url())
        if r.status_code > 500:
            msg = 'PyPI appears to be down. We apologize for the '\
                    'inconvenience. Please retry your upload later.'
            raise forms.ValidationError(msg)
        elif r.status_code > 400:
            msg = 'Could not find this package on PyPI.'
            raise forms.ValidationError(msg)
        elif r.status_code != 200:
            msg = 'Could not validate the existence of this package.'
            raise forms.ValidationError(msg)
        self.instance.pypi_json = r.json()
        return name
