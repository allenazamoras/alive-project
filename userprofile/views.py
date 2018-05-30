from django.contrib.auth import authenticate, login, logout
from rest_framework import views
from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from userprofile.models import User
from livestream.models import Rating
from userprofile.serializers import UserSerializer, RatingSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        req = request.data

        if User.objects.filter(username=req['username']).exists():
            ret = {'return': 'That username is already taken.'}
        else:
            user = User.objects.create_user(username=req['username'],
                                            first_name=req['first_name'],
                                            last_name=req['last_name'],
                                            gender=req['gender'],
                                            password=req['password'])
            user.save()
            ret = {'return': 'Account successfully created.'}
        return Response(ret)


class Login(ObtainAuthToken):

    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        serializer = UserSerializer(user)
        token = Token.objects.get(user=user)
        return Response({'token': token.key,
                         'pk': user.pk,
                         'username': user.username,
                         'first_name': user.first_name,
                         'last_name': user.last_name,
                         'profile_picture': serializer.data['profile_picture']
                         })


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
