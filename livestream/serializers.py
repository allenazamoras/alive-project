from rest_framework import serializers
from .models import Session, User, ClientToken

# SERIALIZERS HERE


class SessionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Session
        fields = ('id', 'session_name', 'session_id')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name')


class ClientTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientToken
        fields = ('user', 'token_id', 'session')
