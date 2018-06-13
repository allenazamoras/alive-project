from django.db.models import Count, Q
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
        fields = ('id', 'username', 'first_name', 'last_name',
                  'profile_picture', 'online')


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
                  'last_name', 'gender', 'profile_picture',
                  'overallrating', 'online', 'openappeals',
                  'closedappeals', 'offers')

    def get_gender(self, obj):
      return obj.get_gender_display()                  

    def get_overallrating(self, obj):
        rate_0 = Count('id', filter=Q(rating=0))
        rate_1 = Count('id', filter=Q(rating=1))
        rate_2 = Count('id', filter=Q(rating=2))
        rate_3 = Count('id', filter=Q(rating=3))
        rate_4 = Count('id', filter=Q(rating=4))
        rate_5 = Count('id', filter=Q(rating=5))

        rating = Rating.objects.filter(user=obj).annotate(rate_0=rate_0)\
            .annotate(rate_1=rate_1).annotate(rate_2=rate_2)\
            .annotate(rate_3=rate_3).annotate(rate_4=rate_4)\
            .annotate(rate_5=rate_5).distinct().first()

        if rating is None:
            return {}
        ret = {i: getattr(rating, 'rate_' + str(i)) for i in range(6)}
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
