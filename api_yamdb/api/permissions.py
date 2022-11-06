#!/api_yamdb/api_yamdb/api/permissions.py
"""All permissions."""
from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(permissions.BasePermission):
    message = 'Пользователь не является администратором!'

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            admin = request.user.role == 'admin'
        else:
            admin = False
        if request.method in permissions.SAFE_METHODS or admin:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        admin = request.user.role == 'admin'
        if request.method in permissions.SAFE_METHODS or admin:
            return True
        return False
