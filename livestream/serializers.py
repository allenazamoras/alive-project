from rest_framework import serializers
from .models import *
from userprofile.models import User

# SERIALIZERS HERE


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password',
                  'first_name', 'last_name',
                  'email', 'date_joined')


class AppealSerializer(serializers.HyperlinkedModelSerializer):
    # nested serialization see drf docu for more info
    owner = UserSerializer()
    helper = UserSerializer()

    class Meta:
        model = Appeal
        fields = ('id', 'request_title', 'session_id', 'detail',
                  'date_pub', 'owner', 'helper', 'is_active')


# class ClientTokenSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ClientToken
#         fields = ('user', 'token_id', 'session')
