from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    """
    Custom permission to only allow superusers to access the view.

    Usage:
        class MyView(APIView):
            permission_classes = [IsSuperUser]
    """
    message = "You must be a superuser to perform this action."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


class IsSuperUserOrReadOnly(BasePermission):
    """
    Custom permission to allow read-only access to any authenticated user,
    but only allow write operations to superusers.

    Usage:
        class MyView(APIView):
            permission_classes = [IsSuperUserOrReadOnly]

    This allows:
    - GET, HEAD, OPTIONS: Any authenticated user
    - POST, PUT, PATCH, DELETE: Only superusers
    """
    message = "You must be a superuser to perform write operations."

    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return bool(request.user and request.user.is_authenticated)

        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)
