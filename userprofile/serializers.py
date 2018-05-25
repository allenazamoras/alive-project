from rest_framework import serializers
from userprofile.models import User
from livestream.models import Appeal
from livestream.serializers import AppealSerializer


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
        offers = AppealSerializer(obj.offers.all(), many=True)
        return offers.data

    def get_openappeals(self, obj):
        appeals = Appeal.objects.filter(owner=obj, is_active=True)
        serializer = AppealSerializer(appeals, many=True)
        return serializer.data

    def get_closedappeals(self, obj):
        appeals = Appeal.objects.filter(owner=obj, is_active=False)
        serializer = AppealSerializer(appeals, many=True)
        return serializer.data
