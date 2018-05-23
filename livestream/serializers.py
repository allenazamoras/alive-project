from rest_framework import serializers
from livestream.models import Appeal, ApprovalRequest
from userprofile.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password',
                  'first_name', 'last_name',
                  'email', 'date_joined', 'reputation')


class AppealSerializer(serializers.HyperlinkedModelSerializer):
    # nested serialization see drf docu for more info
    owner = UserSerializer()
    helper = UserSerializer()

    class Meta:
        model = Appeal
        fields = ('id', 'request_title', 'session_id', 'detail',
                  'date_pub', 'owner', 'helper', 'is_active',
                  'pending_requests')


class ApprovalRequestSerializer(serializers.ModelSerializer):
    appeal = AppealSerializer()
    helper = UserSerializer()

    class Meta:
        model = ApprovalRequest
        fields = ('id', 'helper', 'appeal', 'helper', 'is_approved')

# class ClientTokenSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ClientToken
#         fields = ('user', 'token_id', 'session')
