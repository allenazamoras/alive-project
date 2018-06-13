from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone


class User(AbstractUser):
    """
    Attributes inherited from AbstractUser class
    id, password, last_login, is_superuser, username,
    first_name. last_name, email, is_staff, is_active, date_joined
    """
    GENDER_CHOICES = (
        ('F', 'Female'),
        ('M', 'Male'),
    )
    profile_picture = models.ImageField(upload_to='thumbpath',
                                        default='thumbpath/none/none.jpg')

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='')

    def __str__(self):
        return self.username

    def last_seen(self):
        return cache.get(self.username)

    @property
    def online(self):
        if not self.last_seen():
            return False

        now = timezone.localtime(timezone.now())
        if now > self.last_seen() + timezone.timedelta(
                seconds=settings.USER_ONLINE_TIMEOUT):
            return False
        else:
            return True
