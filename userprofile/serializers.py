from rest_framework import serializers
from userprofile.models import User
from livestream.models import Appeal, Rating, Report


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = ('__all__')


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ('__all__')


class AppealSerializer(serializers.ModelSerializer):
    rating = RatingSerializer(read_only=True, many=True)

    class Meta:
        model = Appeal
        fields = ('id', 'request_title', 'detail', 'date_pub', 'rating')


class UserSerializer(serializers.ModelSerializer):
    overallrating = serializers.SerializerMethodField()
    offers = serializers.SerializerMethodField()
    openappeals = serializers.SerializerMethodField()
    closedappeals = serializers.SerializerMethodField()
    online = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name', 'gender', 'profile_picture',
                  'overallrating', 'online', 'openappeals',
                  'closedappeals', 'offers')

    def get_overallrating(self, obj):
        ret = {
            '0': Rating.objects.filter(user=obj, rating=0).count(),
            '1': Rating.objects.filter(user=obj, rating=1).count(),
            '2': Rating.objects.filter(user=obj, rating=2).count(),
            '3': Rating.objects.filter(user=obj, rating=3).count(),
            '4': Rating.objects.filter(user=obj, rating=4).count(),
            '5': Rating.objects.filter(user=obj, rating=5).count(),
        }
        return ret

    def get_offers(self, obj):
        openappeals = AppealSerializer(obj.offers.exclude(
                                       status=Appeal.INACTIVE), many=True)
        closedappeals = AppealSerializer(
            obj.offers.filter(status=Appeal.INACTIVE), many=True)
        offers = {'openappeals': openappeals.data,
                  'closedappeals': closedappeals.data
                  }
        return offers

    def get_openappeals(self, obj):
        appeals = Appeal.objects.filter(
            owner=obj, status=Appeal.ACTIVE).order_by('date_pub')
        serializer = AppealSerializer(appeals, many=True)
        return serializer.data

    def get_closedappeals(self, obj):
        appeals = Appeal.objects.filter(
            owner=obj, status=Appeal.INACTIVE).order_by('date_pub')
        serializer = AppealSerializer(appeals, many=True)
        return serializer.data

    def get_online(self, obj):
        return obj.online
