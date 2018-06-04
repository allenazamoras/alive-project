from django.views import generic
from rest_framework.response import Response
from rest_framework import status, viewsets

from .models import Appeal, ApprovalRequest
from .serializers import AppealSerializer, ApprovalRequestSerializer
from userprofile.views import NotificationViewSet

from aLive.settings import OPENTOK_API, OPENTOK_SECRET

from opentok import OpenTok, MediaModes

API_KEY = OPENTOK_API
API_SECRET = OPENTOK_SECRET
opentok = OpenTok(API_KEY, API_SECRET)


class AppealViewSet(viewsets.ModelViewSet):
    # permission_classes = (AppealsViewSetPermissions,)
    queryset = Appeal.objects.all()
    serializer_class = AppealSerializer

    def create(self, request, *args, **kwargs):
        session = opentok.create_session(media_mode=MediaModes.routed)
        req = request.data
        if not session:
            return Response({'return': 'Failed to create request'})

        new_session = Appeal(request_title=req['request_title'],
                             session_id=session.session_id,
                             owner=request.user,
                             helper=None,
                             detail=req['detail'],)
        new_session.save()
        return Response({'return': 'Successfully created new request'},
                        status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = Appeal.objects.filter(status=Appeal.AVAILABLE).\
            order_by('date_pub')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        '''
        user will be given a token to connect to this session instance
        '''
        appeal = self.get_object()

        if appeal.status is Appeal.COMPLETED:
            return Response({'return': 'Appeal no longer exists'},
                            status=status.HTTP_404_NOT_FOUND)

        token = opentok.generate_token(appeal.session_id)
        if not token:
            return Response({'return': 'Token creation failed'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = AppealSerializer(appeal, context={'token': token})
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.remove()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ApprovalRequestViewSet(viewsets.ModelViewSet):
    # permission_classes = (ApprovalRequestPermissions,)
    queryset = ApprovalRequest.objects.all()
    serializer_class = ApprovalRequestSerializer

    def create(self, request, *args, **kwargs):
        '''
        an ApprovalRequest instance gets created,
        UNLESS it already exists
        '''
        data = request.data
        appeal_instance = Appeal.objects.get(
            session_id=data['appeal.session_id'])

        if appeal_instance is None:
            return Response({'return': 'request does not exist'})

        if ApprovalRequest.objects.filter(appeal=appeal_instance,
                                          helper=self.request.user).exists():
            if appeal_instance.status is Appeal.COMPLETED:
                # WARNING: if request gets rejected (is_accepted holds false)
                # return message will still be 'pending approval...'
                return Response({'return': 'request no longer exists'},
                                status=status.HTTP_404_NOT_FOUND)
            return Response({'return': 'pending approval...'})

        app_req = ApprovalRequest(appeal=appeal_instance, helper=request.user)
        serializer = ApprovalRequestSerializer(app_req)
        app_req.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def list(self, request, *args, **kwargs):
        '''
        display list of all ApprovalRequests by current user
        should only display ApprovalRequests for
        Appeals that are still AVAILABLE (not in session) and
        Requests that are still PENDING
        '''
        queryset = ApprovalRequest.objects.filter(
            helper=request.user).exclude(status=ApprovalRequest.REJECTED)

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
        # can only be deleted only if it is still pending
        if instance.status == ApprovalRequest.PENDING:
            NotificationViewSet.notify('Cancel', instance)
            self.perform_destroy(instance)
            message = {'return': 'Successfully cancelled pending offer'}
            return Response(message, status=status.HTTP_204_NO_CONTENT)

        message = {'return': 'cannot perform action'}
        return Response(message, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class IndexView(generic.ListView):
    template_name = 'livestream/index.html'
    context_object_name = 'session_list'
    queryset = Appeal.objects.all()
