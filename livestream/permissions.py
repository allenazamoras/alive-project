from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    '''
    To be used for Appeals
    '''
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method == 'GET' and obj.owner == request.user


class IsHelper(BasePermission):
    '''
    To be used for AppealRequest
    '''
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user == obj.helper


class IsOwnerOrHelper(BasePermission):
    def has_object_permission(self, request, view, obj):
        owner = getattr(obj, 'owner', None)
        helper = getattr(obj, 'helper', None)

        return owner == request.user or helper == request.user


class AppealsViewSetPermissions(BasePermission):
    '''
    Authenticated users ['create', 'list']
    Appeal Owner        ['destroy', 'retrieve', 'partial_update', 'update']
    Appeal Helper       ['retrieve']
    '''
    def has_object_permission(self, request, view, obj):
        if request.method in ['POST', 'GET']:
            return request.user.is_authenticated

        if request.method == 'GET':
            owner = getattr(obj, 'owner', None)
            helper = getattr(obj, 'helper', None)

            return owner == request.user or helper == request.user

        if request.method in ['DELETE', 'PATCH', 'PUT']:
            return obj.owner == request.user


class ApprovalRequestPermissions(BasePermission):
    '''
    Authenticated users ['create']
    AR appeal.owner     ['list', 'partial_update', 'retrieve', update]
    AR helper           [all]
    '''
    def has_object_permission(self, request, view, obj):
        if request.method == ['DELETE', 'POST']:
            return not obj.appeal.owner == request.user

        if request.method == ['PATCH', 'PUT']:
            return not obj.helper == request.user

        return request.user.is_authenticated
