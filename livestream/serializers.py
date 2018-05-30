from rest_framework import serializers
from livestream.models import Appeal, ApprovalRequest
from userprofile.models import User


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'profile_picture')


class PendingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalRequest
        fields = ('helper',
                  'status')


class AppealSerializer(serializers.ModelSerializer):
    # nested serialization see drf docu for more info
    owner = BaseUserSerializer()
    helper = HelperSerializer()
    pending_list = serializers.SerializerMethodField()
    token = serializers.SerializerMethodField()

    class Meta:
        model = Appeal
        fields = ('id', 'request_title', 'detail',
                  'date_pub', 'owner', 'helper', 'status',
                  'pending_list', 'session_id', 'token')

    def get_pending_list(self, obj):
        plist = PendingListSerializer(
            obj.approval_requests.filter(
                status=ApprovalRequest.PENDING), many=True)
        return plist.data

    def get_token(self, obj):
        return self.context.get('token', '')


class AppealSerializerForHelpers(serializers.ModelSerializer):
    owner = BaseUserSerializer()

    class Meta:
        model = Appeal
        fields = ('id', 'request_title', 'session_id', 'detail',
                  'date_pub', 'owner', 'status')


class ApprovalRequestSerializer(serializers.ModelSerializer):
    appeal = AppealSerializerForHelpers()
    helper = HelperSerializer()

    class Meta:
        model = ApprovalRequest
        fields = ('id', 'helper', 'appeal', 'status')
