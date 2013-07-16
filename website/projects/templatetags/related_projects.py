from django import template

from ..models import Project


register = template.Library()


@register.inclusion_tag('includes/related_projects.html')
def show_related_projects(package):
    "Renders template with all ralated projects for a given package"
    projects = Project.objects.get_related_projects(package)
    return {'projects': projects}
