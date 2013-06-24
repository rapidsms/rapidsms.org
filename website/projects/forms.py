from django import forms

from .models import Project


class ProjectCreateEditForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('name', 'started', 'countries', 'description', 'challenges',
                'audience', 'technologies', 'metrics', 'num_users',
                'repository_url')
