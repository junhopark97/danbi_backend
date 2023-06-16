from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from account.managers import UserManager


class User(AbstractUser):
    team_choices = (
        ('Danbi', 'Danbi'),
        ('Darae', 'Darae'),
        ('Blabla', 'Blabla'),
        ('Chullo', 'Chullo'),
        ('Ttangi', 'Ttangi'),
        ('Haitai', 'Haitai'),
        ('Sufi', 'Sufi'),
    )

    first_name = None
    last_name = None

    email = models.EmailField(_('email address'), unique=True, help_text='Require')
    team = models.CharField(max_length=10, choices=team_choices)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.email
