from django.contrib.auth import models as auth
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

from website.projects.models import Country


class UserManager(auth.BaseUserManager):

    def create_user(self, email, password, name, **extra_fields):
        now = timezone.now()
        if not all([email, password, name]):
            raise ValueError('Email, password, and name must be given')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, is_staff=False,
                is_active=True, is_superuser=False, last_login=now,
                date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, name, **extra_fields):
        u = self.create_user(email, password, name, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class User(auth.AbstractBaseUser, auth.PermissionsMixin):
    INDIVIDUAL = 'I'
    ORGANIZATION = 'O'
    USER_TYPES = {
        INDIVIDUAL: 'Individual',
        ORGANIZATION: 'Organization',
    }
    user_type = models.CharField(max_length=1, choices=USER_TYPES.items(),
            default=INDIVIDUAL)

    email = models.EmailField('Email address', unique=True)

    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=True, blank=True)
    country = models.ForeignKey(Country, null=True, blank=True)
    website_url = models.URLField(null=True, blank=True)
    github_url = models.URLField(null=True, blank=True)
    for_hire = models.BooleanField(default=False)

    is_staff = models.BooleanField('Staff status', default=False,
            help_text='Designates whether this user can log into the admin site.')
    is_active = models.BooleanField('Active', default=True,
            help_text='Designates whether this user should be treated as '
                'active. Unselect this instead of deleting accounts.')
    date_joined = models.DateTimeField('Date joined', default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('name',)

    def __unicode__(self):
        return self.get_full_name()

    def get_absolute_url(self):
        return reverse('user_detail', args=(self.pk,))

    def get_full_name(self):
        return self.name or self.email

    def get_short_name(self):
        return self.get_full_name()

    def is_individual(self):
        return self.user_type == self.INDIVIDUAL

    def is_organization(self):
        return self.user_type == self.ORGANIZATION
