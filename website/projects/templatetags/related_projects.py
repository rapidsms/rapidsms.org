from django import template

from ..models import Project


register = template.Library()


@register.assignment_tag
def show_related_projects(user_or_package):
    """Renders template with all ralated projects for a given user or
    package"""
    projects = Project.objects.get_related_projects(user_or_package)
    return projects
