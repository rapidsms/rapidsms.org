from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.decorators import method_decorator


class AuthorEditMixin(object):
    """Requires that the requesting user be the object's author.

    For use with Packages and Projects.
    """

    def get_object(self, queryset=None):
        obj = super(AuthorEditMixin, self).get_object(queryset)
        if obj.creator != self.request.user:
            raise Http404()
        return obj


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
