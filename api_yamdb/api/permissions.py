from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS,
    IsAuthenticatedOrReadOnly
)

from users.models import ADMIN, MODERATOR


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.role == 'admin'
                     or request.user.is_superuser))

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and (request.user.role == 'admin'
                     or request.user.is_superuser))


class IsAuthorOrModeratorOrAdminOrReadOnly(IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and (
            obj.author == request.user
            or request.user.role == ADMIN
            or request.user.role == MODERATOR
        )


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.role == ADMIN
                     or request.user.is_superuser))

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and (request.user.role == ADMIN
                     or request.user.is_superuser))


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return (request.user.is_authenticated
                and (request.user.role == ADMIN
                     or request.user.is_superuser))

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return (request.user.is_authenticated
                and (request.user.role == ADMIN
                     or request.user.is_superuser))
