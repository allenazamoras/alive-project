from django.db import models
from django.contrib.auth.models import AbstractUser


class Session(models.Model):
    session_name = models.CharField(max_length=50)
    session_id = models.CharField(max_length=100)

    def __str__(self):
        return self.session_id


class User(AbstractUser):
    session = models.ForeignKey(Session, null=True, on_delete=models.CASCADE,
                                related_name='users')

    def __str__(self):
        return self.username


class ClientToken(models.Model):
    token_id = models.CharField(max_length=500)
    session = models.ForeignKey(Session, on_delete=models.CASCADE,
                                related_name='client_token')
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True)

    def get_session_id(self):
        return self.session.session_id
