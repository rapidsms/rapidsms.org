from django.http import Http404


class AuthorEditMixin(object):
    """Requires that the requesting user be the object's author.

    For use with Packages and Projects.
    """
    def get_object(self, queryset=None):
        obj = super(AuthorEditMixin, self).get_object(queryset)
        if obj.creator != self.request.user:
            raise Http404()
        return obj


class IsActiveMixin(object):
    """Requires that the object(s) displayed be active.

    For use with Packages, Projects, and Users.
    """
    def get_queryset(self):
        queryset = super(IsActiveMixin, self).get_queryset()
        return queryset.filter(is_active=True)
