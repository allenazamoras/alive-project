from django.contrib.auth import authenticate, login
from rest_framework import viewsets
from rest_framework import views
from rest_framework.response import Response
from userprofile.models import User
from userprofile.serializers import UserSerializer


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
                                            password=req['password'])
            user.save()
            ret = {'return': 'Account successfully created.'}
        return Response(ret)


class LoginView(views.APIView):

    def post(self, request, format=None):
        user = authenticate(username=request.data['username'],
                            password=request.data['password'])

        ret = {'return': 'Invalid credentials.'}
        if user is not None:
            login(request, user)
            ret = {'return': 'Logged in.'}
        return Response(ret)
