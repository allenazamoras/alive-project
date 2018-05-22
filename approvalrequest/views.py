from django.shortcuts import render
from rest_framework import viewsets, Response
from rest_framework.response import status
from models import ApprovalRequest
from serializers import ApprovalRequestSerializer


class ApprovalRequestViewSet(viewsets.ModelViewSet):
    queryset = ApprovalRequest
    serializer_class = ApprovalRequestSerializer

    def create(self, request, *args, **kwargs):
        # when user presses "HELP" button
        # an ApprovalRequest instance gets created
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # display list of all ApprovalRequests for that appeal
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        # when a request gets accepted other instances
        # from the same appeal should be deleted
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # when approval request gets rejected it gets deleted from the db
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
