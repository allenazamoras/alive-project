
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Attributes inherited from AbstractUser class
    id, password, last_login, is_superuser, username,
    first_name. last_name, email, is_staff, is_active, date_joined
    """
    profile_picture = models.ImageField(upload_to='thumbpath',
                                        default='thumbpath/none/none.jpg')
    gender = models.CharField(max_length=10, default='')

    def __str__(self):
        return self.username
