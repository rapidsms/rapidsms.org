from optparse import make_option

from django.conf import settings
from django.core.management import BaseCommand, call_command, CommandError

from allaccess.models import Provider


class Command(BaseCommand):
    help = 'Set up a Github provider object for django-allaccess.'
    option_list = BaseCommand.option_list + (
        make_option('--clear',
            action='store_true',
            dest='clear',
            default=False,
            help='Reload Github provider data if it is already present.',
        ),
    )

    def get_provider(self):
        try:
            github = Provider.objects.get(name='github')
        except Provider.DoesNotExist:
            github = None
        return github

    def load_provider(self):
        call_command('loaddata', 'github')
        return self.get_provider()

    def handle(self, *args, **options):
        if not (hasattr(settings, 'GITHUB_KEY') and hasattr(settings, 'GITHUB_SECRET')):
            raise CommandError('GITHUB_KEY and GITHUB_SECRET must be defined '
                    'in your project settings.')

        github = self.get_provider()
        if github:
            self.stdout.write('Existing github provider record found.')
            if options['clear']:
                self.stdout.write('Reloading github provider record.')
                github = self.load_provider()
        else:
            self.stdout.write('No existing github provider record found.')
            self.stdout.write('Loading github provider record.')
            github = self.load_provider()

        if not github:
            raise CommandError('Provider record was not successfully loaded '
                    'from fixture.')

        self.stdout.write('Setting key and secret from project settings.')
        github.key = settings.GITHUB_KEY
        github.secret = settings.GITHUB_SECRET
        github.save()
