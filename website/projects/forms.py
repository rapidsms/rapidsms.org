from django import forms

from selectable.forms import AutoCompleteSelectMultipleField

from .lookups import CountryLookup
from .models import Project


class ProjectCreateEditForm(forms.ModelForm):
    countries = AutoCompleteSelectMultipleField(lookup_class=CountryLookup)

    class Meta:
        model = Project
        fields = ('name', 'started', 'countries', 'description', 'challenges',
                'audience', 'technologies', 'metrics', 'num_users',
                'repository_url')
