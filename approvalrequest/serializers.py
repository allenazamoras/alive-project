from models import ApprovalRequest
from userprofile.serializers import UserSerializer
from livestream.serializers import AppealSerializer
from rest_framework import serializers


class ApprovalRequestSerializer(serializers.ModelSerializer):
    appeal = AppealSerializer()
    helper = UserSerializer()

    class Meta:
        model = ApprovalRequest
        fields = ('id', 'helper', 'appeal', 'helper')
