from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    message = 'Пользователь не является администратором!'

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.role == "admin" or request.user.is_superuser

    # def has_object_permission(self, request, view, obj):
    #     return request.user.is_authenticated and request.user.role == "admin"


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


# class IsSuperUser(permissions.BasePermission):
#     message = 'Пользователь не является суперпользователем!'

#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.is_superuser

#     # def has_object_permission(self, request, view, obj):
#     #     return request.user.is_authenticated and request.user.is_superuser


# class IsOwner(permissions.BasePermission):
#     message = 'Пользователь не является автором!'

#     def has_permission(self, request, view):
#         return request.user.is_authenticated

#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return request.user == obj.author


# class IsModerator(permissions.BasePermission):

#     def has_permission(self, request, view):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return request.user.is_authenticated

#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return request.user.role == "moderator"


class CanPostAndEdit(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
            if request.user.role in ("user", "moderator", "admin", "superuser"):
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user == obj.author:
            return True
        if request.user.role in ("moderator", "admin", "superuser"):
            return True
        if request.user.is_superuser:
            return True
        return False
