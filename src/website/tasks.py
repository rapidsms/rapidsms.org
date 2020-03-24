from django.core.mail import send_mail

from celery import task


@task
def send_email(subject, message, from_email, recipient_list):
    """Send email async using a celery worker

        args: Take sames args as django send_mail function.
    """
    send_mail(subject, message, from_email, recipient_list)
