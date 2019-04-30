import logging

from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """Checks if current user owns object."""
        permitted = False
        logging.info(f'obj.user: {obj.user}')
        logging.info(f'request.user: {request.user}')
        if request.method not in permissions.SAFE_METHODS:
            permitted = obj.user == request.user
        return permitted


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        """Checks if current user is admin."""
        return request.user and request.user.is_staff
