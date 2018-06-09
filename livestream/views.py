from django.views import generic
from rest_framework import status, viewsets, pagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from livestream.models import Appeal, ApprovalRequest, Category
from livestream.serializers import (AppealSerializer,
                                    ApprovalRequestSerializer,
                                    CategorySerializer)
from userprofile.views import NotificationViewSet
from livestream.permissions import (AppealsViewSetPermissions,
                                    ApprovalRequestPermissions,
                                    CategoryPermissions)

from django.conf import settings

from opentok import OpenTok, MediaModes

API_KEY = settings.OPENTOK_API
API_SECRET = settings.OPENTOK_SECRET
opentok = OpenTok(API_KEY, API_SECRET)


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total_pages': self.page.paginator.num_pages,
            'count': self.page.paginator.count,
            'results': data
        })


class AppealViewSet(viewsets.ModelViewSet):
    permission_classes = (AppealsViewSetPermissions,)
    queryset = Appeal.objects.all()
    serializer_class = AppealSerializer
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        if Appeal.objects.filter(owner=request.user,
                                 status=Appeal.AVAILABLE).exists():
            return Response({'return': 'User has too many open Appeals'})

        session = opentok.create_session(media_mode=MediaModes.routed)
        req = request.data
        if not session:
            return Response({'return': 'Failed to create request'})

        if not req['request_title']:
            return Response({'return': 'Cannot create Appeal without a title'})
        if not req['detail']:
            return Response({'return': 'Cannot create Appeal without the details'})

        new_session = Appeal(request_title=req['request_title'],
                             session_id=session.session_id,
                             owner=request.user,
                             helper=None,
                             detail=req['detail'])
        new_session.save()
        new_session.category.add(req['category'])
        return Response({'return': 'Successfully created new request'},
                        status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = Appeal.objects.filter(status=Appeal.AVAILABLE).\
            order_by('-date_pub')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def list_by_category(self, request):
        # TODO
        print("blam")
        req = request.data
        queryset = Appeal.objects.filter(
            status=Appeal.AVAILABLE, category_id=req['category']).\
            order_by('-date_pub')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def add_category(self, request, pk):
        req = request.data
        appeal = self.get_object()
        appeal.category.add(req['category'])
        return Response({'return': 'Category added to appeal'})

    @action(methods=['post'], detail=True)
    def remove_category(self, request, pk):
        req = request.data
        appeal = self.get_object()
        appeal.category.remove(req['category'])
        return Response({'return': 'Category removed from appeal'})

    @action(methods=['post'], detail=True)
    def edit_description(self, request, pk=None):
        # TODO
        appeal = self.get_object()
        serializer = AppealSerializer(appeal)
        if serializer.is_valid():
            appeal.set_description(serializer.data['description'])
            return Response(serializer.data)

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['post'], detail=True)
    def update_status(self, request, pk=None):
        # TODO
        action = request.data['action']
        if action not in ['complete', 'makeunavailable']:
            return Response({'return': 'action impossible'})

        obj = self.queryset.get(pk=pk)

        if not obj:
            return Response({'return': 'Appeal does not exist'})

        success, error = obj.change_status(action)

        if not success:
            return Response(error)

        serializer = AppealSerializer(obj)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def single_appeal(self, request, pk=None):
        obj = self.queryset.get(pk=pk)
        serializer = AppealSerializer(obj)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        '''
        user will be given a token to connect to this session instance
        '''
        appeal = self.get_object()

        if appeal.status not in [Appeal.UNAVAILABLE, Appeal.AVAILABLE]:
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

        if instance.remove():
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'return': 'Appeal is unavailable or no longer exists'})


class ApprovalRequestViewSet(viewsets.ModelViewSet):
    permission_classes = (ApprovalRequestPermissions,)
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

        if ApprovalRequest.objects.filter(
                appeal=appeal_instance,
                status=ApprovalRequest.PENDING).exists():
                message = {'return': 'cannot process request at this moment'}
                return Response(message)

        if appeal_instance.status == Appeal.COMPLETED:
            return Response({'return': 'request no longer exists'},
                            status=status.HTTP_404_NOT_FOUND)

        app_req = ApprovalRequest(appeal=appeal_instance, helper=request.user)
        serializer = ApprovalRequestSerializer(app_req)
        app_req.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    @action(methods=['post'], detail=True)
    def update_status(self, request, pk=None):
        action = request.data['action']

        if action not in ['approve', 'reject']:
            message = {'return': 'action impossible'}
            return Response(message)

        obj = self.queryset.get(pk=pk)
        if not obj:
            return Response({'return': 'Approval request does not exist'})

        success, error = obj.change_status(action)
        if not success:
            return Response({'return': error})
        NotificationViewSet.notify('ApprovalRequest', obj)
        serializer = ApprovalRequestSerializer(obj)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        # when user revokes approval request it gets deleted from the db
        instance = self.get_object()
        # can only be deleted only if it is still pending
        if instance.status in [ApprovalRequest.PENDING, ApprovalRequest.REJECTED]:
            if instance.status == ApprovalRequest.PENDING:
                NotificationViewSet.notify('Cancel', instance)
            self.perform_destroy(instance)
            message = {'return': 'Successfully cancelled offer'}
            return Response(message)

        message = {'return': 'cannot perform action'}
        return Response(message, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (CategoryPermissions,)
