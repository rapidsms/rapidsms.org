from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView,\
        FormView, View
from django.views.generic.detail import SingleObjectMixin

from ..mixins import AuthorEditMixin, IsActiveMixin
from .forms import PackageCreateEditForm, PackageFlagForm
from .models import Package


class PackageCreate(IsActiveMixin, CreateView):
    model = Package
    form_class = PackageCreateEditForm

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(PackageCreate, self).form_valid(form)


class PackageDetail(IsActiveMixin, DetailView):
    model = Package


class PackageEdit(IsActiveMixin, AuthorEditMixin, UpdateView):
    model = Package
    form_class = PackageCreateEditForm


class PackageFlag(IsActiveMixin, SingleObjectMixin, FormView):
    """
    Currently we allow users to freely upload RapidSMS packages to the site.
    In case something gets on there that shouldn't, a user can email an
    administrator through the package flag form.
    """
    model = Package
    form_class = PackageFlagForm
    success_url = reverse_lazy('package_list')
    template_name = 'packages/package_flag.html'
    context_object_name = 'object'  # For consistency with other views.

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(PackageFlag, self).dispatch(request, *args, **kwargs)

    def send_flag_email(self, form):
        # TODO: Make it a Celery task.

        from django.core.mail import send_mail
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

        send_mail(
            subject=subject,
            message=body_text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=settings.FLAG_EMAIL_ALERTS or [],
        )
        return True

    def form_valid(self, form):
        sent = self.send_flag_email(form)
        if sent:
            messages.success(self.request, 'Thanks for flagging {0}. We have '
                    'notified the administrators and they will review this '
                    'package shortly.'.format(self.object))
        else:
            messages.error(self.request, 'Sorry, an error occurred while '
                    'sending the flag email to administrators. Please try '
                    'again later.')
        return super(PackageFlag, self).form_valid(form)


class PackageRefresh(IsActiveMixin, SingleObjectMixin, View):
    """
    User-triggered refresh of the cached PyPI data, especially for use while
    they are re-uploading their own package and want to see what changes
    occurred.
    """
    model = Package
    http_method_names = ['post']

    def refresh_package(self):
        # TODO: Make it a Celery task.
        # Shouldn't execute more than once every minute or so.
        self.object = self.get_object()
        return self.object.update_from_pypi()

    def post(self, request, *args, **kwargs):
        updated = self.refresh_package()
        if updated:
            self.object.save()
            messages.success(self.request, 'The PyPI information for this '
                    'package has been updated.')
        else:
            messages.error(request, 'Sorry, an error occurred while '
                    'updating the information for this package from PyPI. '
                    'Please try again later.')
        return redirect(self.object.get_edit_url())
