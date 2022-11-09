from rest_framework import permissions, exceptions

from blog.models import Post


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsNotAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return False
        else:
            return True


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_staff
        )


class IsPostIdExists(permissions.BasePermission):
    """

    """

    def has_permission(self, request, view):
        post = Post.objects.filter(id=view.kwargs['id'])
        # return bool(post)  # if post exist returns True. Rises 403 exception
        if not post:
            raise exceptions.NotFound()
        return True
