from rest_framework import permissions


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
