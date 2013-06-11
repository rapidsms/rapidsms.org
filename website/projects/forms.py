from django import forms

from .models import Project


class ProjectCreateEditForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('name', 'countries')
