from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from approvalrequest.models import ApprovalRequest
from approvalrequest.serializers import ApprovalRequestSerializer


class ApprovalRequestViewSet(viewsets.ModelViewSet):
    queryset = ApprovalRequest
    serializer_class = ApprovalRequestSerializer

    def create(self, request, *args, **kwargs):
        # when user presses "HELP" button
        # an ApprovalRequest instance gets created,
        # UNLESS it already exists
        appeal_instance = self.request.data['appeal']
        if ApprovalRequest.objects.filter(
            appeal=appeal_instance,
                helper=self.request.user).exists():
            # WARNING: if request gets rejected (is_accepted holds false)
            # return message will still be 'pending approval...'
            return Response({'return': 'pending approval...'})

        # owner should NOT BE ABLE TO create approvalrequess
        # for their OWN appeals, that's stupid
        if appeal_instance.owner == self.request.user:
            return Response({'return': "action impossible"})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def list(self, request, *args, **kwargs):
        # display list of all ApprovalRequests
        # should only display ApprovalRequests that have
        # not been rejected (is_accepted holds null)
        queryset = ApprovalRequest.objects.exclude(is_approved=False)

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
        # when approval request gets rejected it gets deleted from the db
        # when user revokes approval request it gets deleted from the db
        # when a request gets accepted other instances
        # from the same appeal should be deleted
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(serializer.data)
