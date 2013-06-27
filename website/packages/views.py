from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView,\
        FormView, View
from django.views.generic.detail import SingleObjectMixin

from .forms import PackageCreateEditForm, PackageFlagForm
from .models import Package


class PackageEditMixin(object):
    """Users may only edit and delete packages they created."""

    def get_object(self, queryset=None):
        obj = super(PackageEditMixin, self).get_object(queryset)
        if obj.creator != self.request.user:
            raise Http404()
        return obj


class PackageCreate(CreateView):
    model = Package
    form_class = PackageCreateEditForm

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(PackageCreate, self).form_valid(form)


class PackageDetail(DetailView):
    model = Package


class PackageEdit(PackageEditMixin, UpdateView):
    model = Package
    form_class = PackageCreateEditForm


class PackageFlag(SingleObjectMixin, FormView):
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


class PackageRefresh(SingleObjectMixin, View):
    model = Package
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        # TODO: Make it a celery task.
        self.object = self.get_object()
        updated = self.object.update_from_pypi()
        if updated:
            self.object.save()
            messages.success(self.request, 'The PyPI information for this '
                    'package has been updated.')
        else:
            messages.error(request, 'Sorry, an error occurred while '
                    'updating the information for this package from PyPI. '
                    'Please try again later.')
        return redirect(self.object.get_edit_url())
        return super(PackageRefresh, self).post(request, *args, **kwargs)
