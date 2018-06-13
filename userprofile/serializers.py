from django.db.models import Count, Q
from django.conf import settings
from rest_framework import serializers
from userprofile.models import User
from livestream.models import Appeal, Rating, Report, Notification
from livestream.serializers import CategorySerializer


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ('id', 'user', 'seen', 'message', 'icon', 'date_created')


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = ('id', 'user', 'reported_by', 'reason')


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ('id', 'appeal', 'user', 'rating', 'comment',
                  'date_created')


class UserAppealSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name', 'profile_picture_url',
                  'online')


class AppealSerializer(serializers.ModelSerializer):
    rating = RatingSerializer(read_only=True, many=True)
    helper = UserAppealSerializer()
    category = CategorySerializer(many=True)
    owner = UserAppealSerializer()

    class Meta:
        model = Appeal
        fields = ('id', 'request_title', 'detail', 'date_pub', 'rating',
                  'helper', 'category', 'owner')


class UserSerializer(serializers.ModelSerializer):
    overallrating = serializers.SerializerMethodField()
    offers = serializers.SerializerMethodField()
    openappeals = serializers.SerializerMethodField()
    closedappeals = serializers.SerializerMethodField()
    online = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name', 'gender', 'profile_picture_url',
                  'overallrating', 'online', 'openappeals',
                  'closedappeals', 'offers')

    def get_gender(self, obj):
        return obj.get_gender_display()

    def get_overallrating(self, obj):
        ret = {'0': Rating.objects.filter(user=obj, rating=0).count(),
               '1': Rating.objects.filter(user=obj, rating=1).count(),
               '2': Rating.objects.filter(user=obj, rating=2).count(),
               '3': Rating.objects.filter(user=obj, rating=3).count()}
        return ret

    def get_offers(self, obj):
        openappeals = AppealSerializer(obj.offers.exclude(
                                       status=Appeal.AVAILABLE), many=True)
        closedappeals = AppealSerializer(
            obj.offers.filter(status=Appeal.AVAILABLE), many=True)
        offers = {'openappeals': openappeals.data,
                  'closedappeals': closedappeals.data
                  }
        return offers

    def get_openappeals(self, obj):
        appeals = Appeal.objects.filter(
            owner=obj, status=Appeal.AVAILABLE).order_by('date_pub')
        serializer = AppealSerializer(appeals, many=True)
        return serializer.data

    def get_closedappeals(self, obj):
        appeals = Appeal.objects.filter(
            owner=obj, status=Appeal.COMPLETED).order_by('date_pub')
        serializer = AppealSerializer(appeals, many=True)
        return serializer.data

    def get_online(self, obj):
        return obj.online
