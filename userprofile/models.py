import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.cache import cache
from aLive import settings


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

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(
                    seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False
