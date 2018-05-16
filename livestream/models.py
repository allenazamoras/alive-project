from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # red = models.IntegerField()
    """
    Attributes inherited from AbstractUser class
    id, password, last_login, is_superuser, username,
    first_name. last_name, email, is_staff, is_active, date_joined
    """
    reputation = models.PositiveIntegerField(default=0,)
    # is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Appeal(models.Model):
    # Session id
    session_id = models.CharField(max_length=100)
    # Appeal name
    request_title = models.CharField(max_length=50)
    # Additional details for the request
    detail = models.TextField(max_length=500, blank=True)
    # Date and time when the request was published
    date_pub = models.DateTimeField(auto_now_add=True)
    # a request is active when a stream is on going and false if otherwise
    is_active = models.BooleanField(default=False)
    # a request is completed if ... well idk,
    # a request is not completed until the user is satisfied?
    # is_completed = model.BooleanField(default=False)
    # User that created the request
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='requests')
    # User that accepts the request
    helper = models.ForeignKey(User, blank=True, null=True,
                               on_delete=models.SET_NULL,)

    def __str__(self):
        return self.session_id

    def get_description(self):
        return self.detail

# REMOVED to add later when all the world is fixed
# class Rating(models.Model):
#     request = models.OneToOneField(Appeal, on_delete=models.CASCADE,
#                                    primary_key=True)
#     rating = models.PositiveSmallIntegerField(null=True, blank=True)
#     detail = models.TextField(max_length=500, blank=True)


# class Reported(models.Model):
#     request = models.OneToOneField(Appeal, on_delete=models.CASCADE,)
#     reason = models.TextField(max_length=500)


# REMOVED
# REASON: Tokens shouldn't be stored to DB because of their fleeting nature
# class ClientToken(models.Model):
#     token_id = models.CharField(max_length=500)
#     request = models.ForeignKey(Appeal, on_delete=models.CASCADE,
#                                 related_name='client_token')
#     user = models.OneToOneField(User, on_delete=models.CASCADE,
#                                 primary_key=True)

#     def get_session_id(self):
#         return self.request.session_id


# class UserProfile(models.Model):
#     user = models.ForeignKey(User, unique=True)
#     location = models.CharField(max_length=140)
#     gender = models.CharField(max_length=140)
#     employer = models.ForeignKey(Employer)
#     profile_picture = models.ImageField(upload_to='thumbpath', blank=True)

#     def __unicode__(self):
#         return u'Profile of user: %s' % self.user.username
