from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def __str__(self):
        return self.username


class Session(models.Model):
    # Session name
    session_name = models.CharField(max_length=50)
    # Session id
    session_id = models.CharField(max_length=100)
    # User that created the session
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='sessions')

    def __str__(self):
        return self.session_id


class ClientToken(models.Model):
    token_id = models.CharField(max_length=500)
    session = models.ForeignKey(Session, on_delete=models.CASCADE,
                                related_name='client_token')
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True)

    def get_session_id(self):
        return self.session.session_id
