#!/api_yamdb/api_yamdb/api/permissions.py
"""All permissions."""
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    message = 'Пользователь не является администратором!'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated and request.user.role == "admin":
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if (request.method in permissions.SAFE_METHODS
                or request.user.role == 'admin'):
            return True
        return False
