from django.shortcuts import render
from django.views.generic.detail import SingleObjectMixin
from django.views import generic
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action

from .serializers import AppealSerializer, ApprovalRequestSerializer
from .models import Appeal, ApprovalRequest

from aLive.settings import OPENTOK_API, OPENTOK_SECRET

from opentok import OpenTok, MediaModes

API_KEY = OPENTOK_API
API_SECRET = OPENTOK_SECRET
opentok = OpenTok(API_KEY, API_SECRET)


# User can create OpenTok Session
# What if ako ning himuon ug read only
# then mag create ko ug CreateSessionView(CreateAPIView) ?? HUH ?? HUUUH??
class AppealViewSet(SingleObjectMixin, viewsets.ModelViewSet):
    queryset = Appeal.objects.all()
    serializer_class = AppealSerializer
    context = {}

    def create(self, request, *args, **kwargs):

        session = opentok.create_session(media_mode=MediaModes.routed)
        req = request.data
        if session:
            new_session = Appeal(request_title=req['request_title'],
                                 session_id=session.session_id,
                                 owner=request.user,
                                 helper=None,
                                 detail=req['detail'],)
            new_session.save()
            return Response({'return': 'Successfully created new request'},
                            status=status.HTTP_201_CREATED)

        return Response({'return': 'Failed to create request'})

    def list(self, request, *args, **kwargs):
        queryset = Appeal.objects.order_by('date_pub')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        '''
        retrieve method gets called when a user accesses a unique session
        user will be given a token to connect to this session
        '''
        # get current user
        print('i get retrieved')
        user = request.user
        print(user)
        # get current session
        appeal = self.get_object()
        print(appeal)
        # check if session owner ang nag generate sa token
        # or check if puno na ang session (max: 2 publishers)
        # generate token for current user (default: publisher) valid for 24h
        # UMIMPLEMENTED PA ANG CHECKING HAP
        token = opentok.generate_token(appeal.session_id)
        # check if token is created successfully
        print(token)
        self.context = {
            'API_KEY': OPENTOK_API,
            'SESSION_ID': appeal.session_id,
            'TOKEN': token,
        }
        print(self.context)
        # serializer = self.get_serializer(session)
        return render(request, 'livestream/stream.html', self.context)
        # return Response(serializer.data,
        #                 template_name='livestream/stream.html')


class AppealDetailView(generic.DetailView):
    model = Appeal
    template_name = 'livestream/stream.html'

    context = {}

    def get(self, request, *args, **kwargs):
        print("i get rendered")

        user = request.user
        print(user)
        # get current session
        appeal = self.get_object()
        print(appeal)
        # check if session owner ang nag generate sa token
        # or check if puno na ang session (max: 2 publishers)
        # generate token for current user (default: publisher) valid for 24h
        # UMIMPLEMENTED PA ANG CHECKING HAP
        token = opentok.generate_token(appeal.session_id)
        # check if token is created successfully
        print(token)
        self.context = {
            'API_KEY': OPENTOK_API,
            'SESSION_ID': appeal.session_id,
            'TOKEN': token,
        }
        print(self.context)

        return self.render_to_response(self.context)


class ApprovalRequestViewSet(viewsets.ModelViewSet):
    queryset = ApprovalRequest.objects.all()
    serializer_class = ApprovalRequestSerializer

    def create(self, request, *args, **kwargs):
        # when user presses "HELP" button
        # an ApprovalRequest instance gets created,
        # UNLESS it already exists
        appeal_instance = self.request.data['appeal']
        # owner should NOT BE ABLE TO create approvalrequess
        # for their OWN appeals
        if appeal_instance.owner == self.request.user:
            return Response({'return': 'action impossible'})
        
        if ApprovalRequest.objects.filter(appeal=appeal_instance,
                                          helper=self.request.user).exists():
            if appeal_instance.is_active is True:
                # WARNING: if request gets rejected (is_accepted holds false)
                # return message will still be 'pending approval...'
                return Response({'return': 'pending approval...'})
            else:
                return Response({'return': 'request no longer exists'},
                                status=status.HTTP_404_DOES_NOT_EXIST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def list(self, request, *args, **kwargs):
        # display list of all ApprovalRequests by current user
        # should only display ApprovalRequests that have
        # not been rejected (is_accepted holds null)
        queryset = ApprovalRequest.objects.filter(helper=request.user).\
            exclude(is_approved=False)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # when user revokes approval request it gets deleted from the db
        instance = self.get_object()
        instance_appeal = instance.appeal
        user_inst = request.user
        message = {'return': 'You cannot delete this instance'}
        # request instance can only be deleted by
        # user who offered help
        if instance.helper == user_inst:
            self.perform_destroy(instance)
            message['return'] = 'Successfully cancelled pending offer'
            return Response(message, status=status.HTTP_204_NO_CONTENT)
        return Response(message, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class IndexView(generic.ListView):
    template_name = 'livestream/index.html'
    context_object_name = 'session_list'
    queryset = Appeal.objects.all()
