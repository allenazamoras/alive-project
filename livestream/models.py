from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
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

    INACTIVE = 'INACTIVE'
    ACTIVE = 'ACTIVE'
    COMPLETED = 'COMPLETED'

    STATUS = (
        (INACTIVE, 'inactive'),
        (ACTIVE, 'active'),
        (COMPLETED, 'completed'),
    )

    # Session id
    session_id = models.CharField(max_length=100)
    # Appeal name
    request_title = models.CharField(max_length=50)
    # Additional details for the request
    detail = models.TextField(max_length=500, blank=True)
    # Date and time when the request was published
    date_pub = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=9,
                              choices=STATUS, default=INACTIVE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='requests')
    # User that accepts the request
    helper = models.ForeignKey(User, blank=True, null=True,
                               on_delete=models.SET_NULL,
                               related_name='offers')
    category = models.CharField(max_length=20,
                                choices=CATEGORY, default=OTHERS)

    def __str__(self):
        return self.request_title

    def get_description(self):
        return self.detail

    def activate(self):
        self.status = self.ACTIVE

    def deactivate(self):
        self.status = self.INACTIVE


class ApprovalRequest(models.Model):
    PENDING = 'p'
    REJECTED = 'r'
    APPROVED = 'a'

    STATUS = (
        (PENDING, 'pending'),
        (REJECTED, 'rejected'),
        (APPROVED, 'approved'),
    )

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


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='ratings')
    appeal = models.ForeignKey(Appeal, on_delete=models.CASCADE,
                               related_name='ratings')
    rating = models.IntegerField(validators=[MinValueValidator(0),
                                             MaxValueValidator(5)])


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='reported_user')
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                    related_name='reported_by')
    reason = models.CharField(max_length=255, blank=True)
