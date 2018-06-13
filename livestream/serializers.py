from rest_framework import serializers
from livestream.models import Appeal, ApprovalRequest, Category
from userprofile.models import User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'first_name',
                  'last_name',
                  'profile_picture_url',
                  'online')


class PendingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalRequest
        fields = ('helper',
                  'status')


class AppealSerializer(serializers.HyperlinkedModelSerializer):
    # nested serialization see drf docu for more info
    owner = UserSerializer()
    helper = UserSerializer()
    pending_list = serializers.SerializerMethodField()
    token = serializers.SerializerMethodField()
    category = CategorySerializer(many=True)

    class Meta:
        model = Appeal
        fields = ('id', 'request_title', 'detail', 'category',
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

    owner = UserSerializer()

    class Meta:
        model = Appeal
        fields = ('id', 'request_title', 'session_id', 'detail',
                  'date_pub', 'owner', 'status')


class ApprovalRequestSerializer(serializers.ModelSerializer):
    appeal = AppealSerializerForHelpers()
    helper = UserSerializer()

    class Meta:
        model = ApprovalRequest
        fields = ('id', 'helper', 'appeal', 'status')


class SearchSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    helper = UserSerializer()

    class Meta:
        model = Appeal
        fields = ('id', 'request_title', 'detail',
                  'date_pub', 'owner', 'helper', 'session_id')
