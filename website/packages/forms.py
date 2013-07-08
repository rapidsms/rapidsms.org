from django import forms

from .models import Package


class PackageCreateEditForm(forms.ModelForm):
    # Use a radio select field rather than the default.
    pkg_type = forms.ChoiceField(label='Package Type',
            widget=forms.RadioSelect, choices=Package.PACKAGE_TYPES.items())

    class Meta:
        model = Package
        fields = ('pkg_type', 'name', 'tests_url', 'repo_url')

    def __init__(self, *args, **kwargs):
        super(PackageCreateEditForm, self).__init__(*args, **kwargs)

        # Package type and name are not editable once the project has been
        # created.
        if self.instance.pk:
            self.fields.pop('pkg_type')
            self.fields.pop('name')

    def clean_name(self):
        """
        Ensure that a package with the given name is on PyPI, and add
        PyPI-derived data to the instance.

        Creates its own request to pass into update_from_pypi, in order to
        save an RTT.
        """
        name = self.cleaned_data['name']
        self.instance.name = name
        req = self.instance._get_pypi_request()
        if req.status_code >= 500:
            msg = 'PyPI appears to be down. We apologize for the '\
                    'inconvenience. Please retry your upload later.'
            raise forms.ValidationError(msg)
        elif req.status_code > 400:
            msg = 'Could not find this package on PyPI.'
            raise forms.ValidationError(msg)
        elif req.status_code != 200:
            msg = 'Could not validate the existence of this package.'
            raise forms.ValidationError(msg)
        self.instance.update_from_pypi(req)
        return name


class PackageFlagForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea,
            label='Reason for Flagging')
