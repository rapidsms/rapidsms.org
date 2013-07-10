from celery import task
from django.core.mail import send_mail


@task
def send_email(subject, message, from_email, recipient_list):
    """Send email async using a celery worker

        args: Take sames args as django send_mail function.
    """
    send_mail(subject, message, from_email, recipient_list)


@task
def update_package(package):
    """Updates a single package from pypi.

        args: takes a packages instance as a single argument.
    """
    package.update_from_pypi()
    package.save()


@task
def update_packages():
    """Updates all active packages."""

    from .models import Package

    packages = Package.objects.active_packages()
    for package in packages:
        packages.update_from_pypi()
