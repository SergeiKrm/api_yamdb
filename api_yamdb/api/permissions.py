from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrModeratorOrAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            or request.method in SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and (
            obj.author == request.user
            or request.user.role == 'admin'
            or request.user.role == 'moderator'
        )


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.role == 'admin'
                     or request.user.is_superuser))

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and (request.user.role == 'admin'
                     or request.user.is_superuser))


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return (request.user.is_authenticated
                and (request.user.role == 'admin'
                     or request.user.is_superuser))

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return (request.user.is_authenticated
                and (request.user.role == 'admin'
                     or request.user.is_superuser))
