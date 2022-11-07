#!/api_yamdb/api_yamdb/api/permissions.py
"""All permissions."""
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    message = 'Пользователь не является администратором!'

    def has_permission(self, request, view):
        is_admin = False
        if not request.user.is_anonymous:
            is_admin = request.user.role == 'admin'
        if request.method in permissions.SAFE_METHODS or is_admin:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        admin = request.user.role == 'admin'
        if request.method in permissions.SAFE_METHODS or admin:
            return True
        return False
