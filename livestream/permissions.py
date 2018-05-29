from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    '''
    To be used for Appeals
    '''
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return view.action == 'retrieve' and obj.owner == request.user


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

    def has_permission(self, request, view):
        return view.action in ['create', 'list'] and \
            request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return IsOwnerOrHelper.has_object_permission(
                self, request, view, obj)

        if view.action in ['destroy', 'partial_update', 'update']:
            return obj.owner == request.user


class ApprovalRequestPermissions(BasePermission):
    '''
    Authenticated users ['create']
    AR appeal.owner     ['list', 'partial_update', 'retrieve', update]
    AR helper           [all]
    '''
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if view.action == ['destroy', 'create']:
            return not obj.appeal.owner == request.user

        if view.action == ['partial_update', 'update']:
            return not obj.helper == request.user
