from rest_framework import serializers
from livestream.models import Appeal, ApprovalRequest
from userprofile.models import User


class OwnerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username',
                  'first_name', 'last_name',
                  'profile_picture')


class HelperSerializer(serializers.HyperlinkedModelSerializer):
    reputation = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username',
                  'first_name', 'last_name',
                  'profile_picture', )

    def get_reputation(self, obj):
        # TO DO when user rating is up
        return ''


class PendingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalRequest
        fields = ('helper', 'is_approved')


class AppealSerializer(serializers.HyperlinkedModelSerializer):
    # nested serialization see drf docu for more info
    owner = OwnerSerializer()
    helper = HelperSerializer()
    pending_list = serializers.SerializerMethodField()
    token = serializers.SerializerMethodField()

    class Meta:
        model = Appeal
        fields = ('id', 'request_title', 'session_id', 'detail',
                  'date_pub', 'owner', 'helper', 'is_active',
                  'pending_list', 'token')

    def get_pending_list(self, obj):
        plist = PendingListSerializer(
            obj.approval_requests.filter(is_approved=None), many=True)
        return plist.data

    def get_token(self, obj):
        return self.context.get('token', '')


class AppealSerializerForHelpers(serializers.HyperlinkedModelSerializer):
    owner = OwnerSerializer()

    class Meta:
        model = Appeal
        fields = ('id', 'request_title', 'session_id', 'detail',
                  'date_pub', 'owner', 'is_active')


class ApprovalRequestSerializer(serializers.ModelSerializer):
    appeal = AppealSerializerForHelpers()
    helper = HelperSerializer()

    class Meta:
        model = ApprovalRequest
        fields = ('id', 'helper', 'appeal', 'is_approved')
