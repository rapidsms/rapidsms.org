import datetime

from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView,\
        FormView, View
from django.views.generic.detail import SingleObjectMixin

from ..mixins import AuthorEditMixin, IsActiveObjectMixin, LoginRequiredMixin
from .forms import PackageCreateEditForm, PackageFlagForm
from .models import Package
from .tasks import update_package
from website.tasks import send_email


class PackageCreate(LoginRequiredMixin, CreateView):
    model = Package
    form_class = PackageCreateEditForm

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(PackageCreate, self).form_valid(form)


class PackageDetail(IsActiveObjectMixin, DetailView):
    model = Package


class PackageEdit(LoginRequiredMixin, IsActiveObjectMixin, UpdateView):
    model = Package
    form_class = PackageCreateEditForm


# TODO: This probably doesn't need to require login. But in that case we may
# want to integrate something like honeypot at least.
class PackageFlag(LoginRequiredMixin, IsActiveObjectMixin, SingleObjectMixin,
        FormView):
    """
    Currently we allow users to freely upload RapidSMS packages to the site.
    In case something gets on there that shouldn't, a user can email an
    administrator through the package flag form.
    """
    model = Package
    form_class = PackageFlagForm
    template_name = 'packages/package_flag.html'
    context_object_name = 'object'  # For consistency with other views.

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(PackageFlag, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.object.get_absolute_url()

    def send_flag_email(self, form):
        # TODO: Make it a Celery task.

        from django.template import Context, loader
        from django.conf import settings

        context = Context({
            'user': self.request.user,
            'user_url': self.request.build_absolute_uri(
                    self.request.user.get_absolute_url()),
            'package': self.object,
            'package_url': self.request.build_absolute_uri(
                    self.object.get_absolute_url()),
            'reason': form.cleaned_data['reason'],
        })

        subject_template = 'packages/flag_email/subject.txt'
        body_text_template = 'packages/flag_email/body.txt'

        subject = loader.render_to_string(subject_template, context)
        subject = ''.join(subject.splitlines())
        body_text = loader.render_to_string(body_text_template, context)
        #sending email is delegated to celery
        send_email.delay(
            subject=subject,
            message=body_text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=settings.FLAG_EMAIL_ALERTS or [],
        )
        return True

    def form_valid(self, form):
        self.object.is_flagged = True
        self.object.save(update_fields=['is_flagged'])
        self.send_flag_email(form)
        # email is sent async, no time to wait for the response
        messages.success(self.request, 'Thanks for flagging {0}. We have '
            'notified the administrators and they will review this '
            'package shortly.'.format(self.object))
        return super(PackageFlag, self).form_valid(form)


class PackageRefresh(LoginRequiredMixin, IsActiveObjectMixin,
        SingleObjectMixin, View):
    """
    User-triggered refresh of the cached PyPI data, especially for use while
    they are re-uploading their own package and want to see what changes
    occurred.
    """
    model = Package
    http_method_names = ['post']

    @staticmethod
    def refresh_package(package):
        # TODO: Make it a Celery task.
        # Shouldn't execute more than once every minute or so.
        # Package update is delegated to celery.
        update_package(package)

    def post(self, request, *args, **kwargs):
        package = self.get_object()
        now = timezone.now()
        last_updated = package.pypi_updated
        needs_update = (now - last_updated > datetime.timedelta(minutes=1))
        if needs_update:
            self.refresh_package(package)
            messages.success(self.request, 'Your package will be '
                'updated shortly.')
        else:
            messages.error(request, 'Your package can only be updated once '
                'every minute.')
        return redirect(package.get_edit_url())
