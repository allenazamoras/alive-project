from rest_framework import serializers
from .models import *

# SERIALIZERS HERE


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password',
                  'first_name', 'last_name',
                  'email', 'date_joined', 'reputation')


class RequestSerializer(serializers.HyperlinkedModelSerializer):
    # nested serialization see drf docu for more info
    owner = UserSerializer()
    helper = UserSerializer()

    class Meta:
        model = Request
        fields = ('id', 'request_title', 'session_id',
                  'owner', 'helper', 'detail', 'date_pub',
                  'is_active')


# class ClientTokenSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ClientToken
#         fields = ('user', 'token_id', 'session')
