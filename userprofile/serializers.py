from rest_framework import serializers
from userprofile.models import User
from livestream.models import Appeal, ApprovalRequest


class BaseAppealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appeal
        fields = ('request_title', 'detail',)


class OpenAppealSerializer(BaseAppealSerializer):
    class Meta:
        model = Appeal
        fields = BaseAppealSerializer.Meta.fields + ('date_pub',)


class OfferSerializer(serializers.ModelSerializer):
    appeal = OpenAppealSerializer()

    class Meta:
        model = ApprovalRequest
        fields = ('appeal', 'is_approved')


class UserSerializer(serializers.ModelSerializer):
    offers = serializers.SerializerMethodField()
    openappeals = serializers.SerializerMethodField()
    closedappeals = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name',
                  'last_name', 'gender', 'profile_picture',
                  'openappeals', 'closedappeals', 'offers')

    def get_offers(self, obj):
        offers = OpenAppealSerializer(obj.offers.all(), many=True)
        return offers.data

    def get_openappeals(self, obj):
        appeals = Appeal.objects.filter(owner=obj, is_active=None)
        serializer = OpenAppealSerializer(appeals, many=True)
        return serializer.data

    def get_closedappeals(self, obj):
        appeals = Appeal.objects.filter(owner=obj, is_active=False)
        serializer = BaseAppealSerializer(appeals, many=True)
        return serializer.data
