from rest_framework import serializers
from .models import Session, User, ClientToken

# SERIALIZERS HERE


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name')


class SessionSerializer(serializers.HyperlinkedModelSerializer):
    # nested serialization see drf docu for more info
    owner = UserSerializer()

    class Meta:
        model = Session
        fields = ('id', 'session_name', 'session_id', 'owner')


class ClientTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientToken
        fields = ('user', 'token_id', 'session')
