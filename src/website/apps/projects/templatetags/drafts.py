from django import template

from ..models import Project

register = template.Library()


@register.simple_tag
def count_drafts(request):
    """Returns the number of drafts current user has."""
    if request.user.is_authenticated:
        drafts = Project.objects.get_drafts_for_user(request.user)
        return drafts.count()
    return None


@register.inclusion_tag('includes/drafts.html')
def show_drafts(request):
    "Render template with context variable 'projects'"
    # drafts current user can edit.
    if request.user.is_authenticated:
        drafts = Project.objects.get_drafts_for_user(request.user)
        return {"projects": drafts}
