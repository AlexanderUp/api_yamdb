#!/api_yamdb/api_yamdb/api/permissions.py
"""All permissions."""
from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    message = 'Пользователь не является администратором!'

    def has_permission(self, request, view):
        user = request.user
        is_admin = request.user.role == 'admin'
        return (
            user.is_authenticated and is_admin
        )


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        admin = request.user.role == 'admin'
        if request.method in permissions.SAFE_METHODS or admin:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        admin = request.user.role == 'admin'
        if request.method in permissions.SAFE_METHODS or admin:
            return True
        return False
