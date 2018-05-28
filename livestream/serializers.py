from rest_framework import serializers
from livestream.models import Appeal, ApprovalRequest
from userprofile.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username',
                  'first_name', 'last_name',
                  'profile_picture')


class PendingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalRequest
        fields = ('helper', 'is_approved')


class AppealSerializer(serializers.HyperlinkedModelSerializer):
    # nested serialization see drf docu for more info
    owner = UserSerializer()
    helper = UserSerializer()
    pending_list = serializers.SerializerMethodField()

    class Meta:
        model = Appeal
        fields = ('id', 'request_title', 'session_id', 'detail',
                  'date_pub', 'owner', 'helper', 'is_active',
                  'pending_list')

    def get_pending_list(self, obj):
        plist = PendingListSerializer(
            obj.approval_requests.filter(is_approved=None), many=True)
        return plist.data


class AppealSerializerForHelpers(serializers.HyperlinkedModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = Appeal
        fields = ('id', 'request_title', 'session_id', 'detail',
                  'date_pub', 'owner', 'is_active')


class ApprovalRequestSerializer(serializers.ModelSerializer):
    appeal = AppealSerializerForHelpers()
    helper = UserSerializer()

    class Meta:
        model = ApprovalRequest
        fields = ('id', 'helper', 'appeal', 'is_approved')
