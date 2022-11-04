from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.role == "admin" or request.user.is_superuser

    # def has_object_permission(self, request, view, obj):
    #     return request.user.is_authenticated and request.user.role == "admin"


class IsSuperUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser

    # def has_object_permission(self, request, view, obj):
    #     return request.user.is_authenticated and request.user.is_superuser
