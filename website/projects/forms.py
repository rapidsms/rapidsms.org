from django import forms
from selectable.forms import AutoCompleteSelectMultipleField

from ..packages.lookups import PackageLookup
from .lookups import CountryLookup
from .models import Project
from website.taxonomy.lookups import TaxonomyLookup
from website.users.lookups import UserLookup


class ProjectCreateEditForm(forms.ModelForm):
    countries = AutoCompleteSelectMultipleField(lookup_class=CountryLookup)
    packages = AutoCompleteSelectMultipleField(lookup_class=PackageLookup,
        required=False)
    tags = AutoCompleteSelectMultipleField(lookup_class=TaxonomyLookup,
        required=False)
    collaborators = AutoCompleteSelectMultipleField(lookup_class=UserLookup,
        required=False)

    class Meta:
        model = Project
        fields = ('name', 'description', 'countries', 'tags',
                'challenges', 'audience', 'technologies', 'metrics',
                'num_users', 'started', 'packages', 'collaborators',
                'repository_url', 'project_url', 'image', 'files')
