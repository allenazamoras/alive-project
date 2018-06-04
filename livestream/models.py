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

    AVAILABLE = 'a'
    UNAVAILABLE = 'u'
    COMPLETED = 'c'
    REMOVED = 'r'

    STATUS = (
        (AVAILABLE, 'available'),
        (UNAVAILABLE, 'unavailable'),
        (COMPLETED, 'completed'),
        (REMOVED, 'removed'),
    )

    # Session id
    session_id = models.CharField(max_length=100)
    # Appeal name
    request_title = models.CharField(max_length=50)
    # Additional details for the request
    detail = models.TextField(max_length=500, blank=True)
    # Date and time when the request was published
    date_pub = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1,
                              choices=STATUS, default=AVAILABLE)
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

    def set_description(self, description):
        self.description = description
        self.save()

    def set_available(self):
        self.status = self.AVAILABLE
        self.save()

    def set_unavailable(self):
        if not self.status == self.AVAILABLE:
            return False

        self.status = self.UNAVAILABLE
        self.save()
        return True

    def completed(self):
        if self.status == self.UNAVAILABLE:
            return False

        self.status = self.COMPLETED
        self.save()
        return True

    def remove(self):
        if self.status == self.AVAILABLE:
            return False

        self.status = self.REMOVED
        self.save()
        return True


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
    status = models.CharField(max_length=1,
                              choices=STATUS, default=PENDING)

    def __str__(self):
        to_string = {'Request Title': self.appeal.request_title,
                     'Helper': self.helper.username}
        return str(to_string)

    def approve(self):
        if self.status == self.PENDING:
            self.status = self.APPROVED
            self.appeal.helper = self.helper
            self.appeal.status = Appeal.UNAVAILABLE
            self.appeal.save()
            self.save()

    def reject(self):
        if self.status == self.PENDING:
            self.status = self.REJECTED
            self.save()


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='rating')
    appeal = models.ForeignKey(Appeal, on_delete=models.CASCADE,
                               related_name='rating')
    rating = models.IntegerField(validators=[MinValueValidator(0),
                                             MaxValueValidator(5)])


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='reported_user')
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                    related_name='reported_by')
    reason = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username
