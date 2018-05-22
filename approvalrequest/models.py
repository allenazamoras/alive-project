from django.db import models
from livestream.models import Appeal
from userprofile.models import User


class ApprovalRequest(models.Model):
    appeal = models.ForeignKey(Appeal, on_delete=models.CASCADE,
                               related_name='approval_requests')
    helper = models.OneToOneField(User, on_delete=models.CASCADE)
    is_approved = models.NullBooleanField()

    def __str__(self):
        to_string = {'Request Title': self.appeal.request_title,
                     'Helper': self.helper.username}
        return str(to_string)
