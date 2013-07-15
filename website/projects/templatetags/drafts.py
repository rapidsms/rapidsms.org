from django import template

from ..models import Project


register = template.Library()


@register.inclusion_tag('includes/drafts.html')
def show_drafts(request):
    "Render template with context variable 'projects'"
    # drafts current user can edit.
    # import pdb; pdb.set_trace()
    drafts = Project.objects.get_drafts_for_user(request.user)
    return {"projects": drafts}


@register.assignment_tag
def count_drafts(request):
    """Returns the number of drafts current user has."""
    drafts = Project.objects.get_drafts_for_user(request.user)
    return drafts.count()
