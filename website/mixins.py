from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator


class AuthorEditMixin(object):
    """Requires that the requesting user be the object's author.

    For use with Packages and Projects.
    """

    def get_object(self, queryset=None):
        obj = super(AuthorEditMixin, self).get_object(queryset)
        if obj.creator != self.request.user:
            raise PermissionDenied
        return obj


class CanEditMixin(object):
    """Check user permission for current object.

    Views using the mixin need to make sure that underlaying Model
    implement a can_edit method.

    e.g.

    def can_edit(self, user):
        "Check if a user has rights to edit this instance"
        if user == self.creator or user in self.collaborators:
            return True
    """

    def get_object(self, queryset=None):
        """Return obj if user can edit it else raises a
        PermissionDenied exception.

        """
        obj = super(CanEditMixin, self).get_object(queryset)
        user_can_edit = obj.can_edit(self.request.user)
        if user_can_edit:
            return obj
        raise PermissionDenied


class IsActiveObjectMixin(object):
    """Requires that the object(s) displayed be active.

    For use with Packages, Projects, and Users.
    """

    def get_queryset(self):
        queryset = super(IsActiveObjectMixin, self).get_queryset()
        return queryset.filter(is_active=True)


class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)
