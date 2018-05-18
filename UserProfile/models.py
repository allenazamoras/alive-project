from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser

from rest_framework.authtoken.models import Token


class User(AbstractUser):
    """
    Attributes inherited from AbstractUser class
    id, password, last_login, is_superuser, username,
    first_name. last_name, email, is_staff, is_active, date_joined
    """

    reputation = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.username


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
