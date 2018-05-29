from rest_framework import serializers
from userprofile.models import User
from livestream.models import Appeal


class AppealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appeal
        fields = ('request_title', 'detail', 'date_pub',)


class UserSerializer(serializers.ModelSerializer):
    offers = serializers.SerializerMethodField()
    openappeals = serializers.SerializerMethodField()
    closedappeals = serializers.SerializerMethodField()
    online = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name', 'gender', 'profile_picture',
                  'online', 'openappeals', 'closedappeals', 'offers')

    def get_offers(self, obj):

        openappeals = AppealSerializer(obj.offers.exclude(is_active=False),
                                       many=True)
        closedappeals = AppealSerializer(
            obj.offers.filter(is_active=False), many=True)
        offers = {'openappeals': openappeals.data,
                  'closedappeals': closedappeals.data
                  }
        return offers

    def get_openappeals(self, obj):
        appeals = Appeal.objects.filter(owner=obj,
                                        is_active=True).order_by('date_pub')
        serializer = AppealSerializer(appeals, many=True)
        return serializer.data

    def get_closedappeals(self, obj):
        appeals = Appeal.objects.filter(owner=obj,
                                        is_active=False).order_by('date_pub')
        serializer = AppealSerializer(appeals, many=True)
        return serializer.data

    def get_online(self, obj):
        return obj.online
