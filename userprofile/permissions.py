from rest_framework import permissions
from rest_framework.permissions import BasePermission


class UserViewSetPermissions(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        elif request.method in ['PUT', 'PATCH']:
            return request.user == obj
        elif request.method == 'POST':
            return True
