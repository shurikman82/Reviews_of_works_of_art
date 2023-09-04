from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser)


class AdminAuthorModeratorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )


    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_moderator
            or request.iser.is_admin
            or request.iser.is_superuser
            or request.user == obj.author
        ) or request.method in permissions.SAFE_METHODS
