from rest_framework import permissions


class IsAccountOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        List only for admin
        """
        if request.user.is_superuser:
            return True
        if view.action == "list":
            return False

        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        return obj.user == request.user
