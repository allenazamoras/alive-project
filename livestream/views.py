from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from rest_framework.response import Response
from rest_framework import status, viewsets

from .serializers import *
from .models import Session, User

from aLive.settings import OPENTOK_API, OPENTOK_SECRET

from opentok import OpenTok

API_KEY = OPENTOK_API
API_SECRET = OPENTOK_SECRET
opentok = OpenTok(API_KEY, API_SECRET)


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

    def create(self, request, *args, **kwargs):
        session = opentok.create_session()
        req = request.data
        if session:
            new_session = Session(session_name=req['session_name'],
                                  session_id=session.session_id)
            new_session.save()
            return Response({'return': 'Successfully created new session'},
                            status=status.HTTP_201_CREATED)

        return Response({'return': 'Failed to create session'})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        req = request.data
        user = User.object.create_user(username=req['username'],
                                       password=req['password'],
                                       firstname=req['first_name'],
                                       lastname=req['last_name'])
        if user:
            user.save()
            return Response(request.data, status=status.HTTP_201_CREATED)

        return Response({'return': 'Failed to create new user.'})

    def is_publishing():
        # code to check if publishing si user
        pass

    def is_subscribed():
        # code to check if subscribed ba si user
        pass


class ClientTokenViewSet(viewsets.ModelViewSet):
    queryset = ClientToken.objects.all()
    serializer_class = ClientTokenSerializer

    def create(self, request):
        ret = {'return': 'token creation failed'}
        req = request.data
        # get session id from db
        this_session = Session.objects.get(id=req['session'])
        # generate token
        token = opentok.generate_token(this_session.session_id)
        # get user
        user = User.objects.get(id=req['user'])
        new_token = ClientToken(token_id=token,
                                # fixed wrong parameter thingy
                                session=this_session,
                                user=user)
        # check if new token was successfully created
        # and user does not have existing token
        print(ClientTokenSerializer(new_token).data)
        if new_token and not ClientToken.objects.get(user=user):
            print(new_token)
            # Value error here
            new_token.save()
            # VALUE ERROR SOLVED
            ret = ClientTokenSerializer(new_token).data

        return Response(ret)
