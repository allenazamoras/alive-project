from django.db import models
from userprofile.models import User


class Appeal(models.Model):
    OTHERS = 'OTHERS'
    PERSONAL = 'PERSONAL'
    FAMILY = 'FAMILY'
    WORK = 'WORK'
    SCHOOL = 'SCHOOL'
    RELATIONSHIP = 'RELATIONSHIP'

    CATEGORY = (
        (OTHERS, 'others'),
        (PERSONAL, 'personal'),
        (FAMILY, 'family'),
        (WORK, 'work'),
        (SCHOOL, 'school'),
        (RELATIONSHIP, 'relationship'),
    )

    # Session id
    session_id = models.CharField(max_length=100)
    # Appeal name
    request_title = models.CharField(max_length=50)
    # Additional details for the request
    detail = models.TextField(max_length=500, blank=True)
    # Date and time when the request was published
    date_pub = models.DateTimeField(auto_now_add=True)
    # holds null by default
    # holds true when appeal is being addressed
    # holds false when appeal is completed/closed/deleted
    is_active = models.NullBooleanField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='requests')
    # User that accepts the request
    helper = models.ForeignKey(User, blank=True, null=True,
                               on_delete=models.SET_NULL,
                               related_name='offers')
    category = models.CharField(max_length=20,
                                choices=CATEGORY, default=OTHERS)

    def __str__(self):
        return self.session_id

    def get_description(self):
        return self.detail

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False


class ApprovalRequest(models.Model):
    appeal = models.ForeignKey(Appeal, on_delete=models.CASCADE,
                               related_name='approval_requests')
    helper = models.ForeignKey(User, on_delete=models.CASCADE)
    # holds null if pending, false if rejected
    # true if accepted/approved
    is_approved = models.NullBooleanField()

    def __str__(self):
        to_string = {'Request Title': self.appeal.request_title,
                     'Helper': self.helper.username}
        return str(to_string)


# REMOVED to add later when all the world is fixed
# class Rating(models.Model):
#     request = models.OneToOneField(Appeal, on_delete=models.CASCADE,
#                                    primary_key=True)
#     rating = models.PositiveSmallIntegerField(null=True, blank=True)
#     detail = models.TextField(max_length=500, blank=True)


# class Reported(models.Model):
#     request = models.OneToOneField(Appeal, on_delete=models.CASCADE,)
#     reason = models.TextField(max_length=500)
