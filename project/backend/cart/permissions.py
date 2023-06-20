from rest_framework import permissions


class IsAdminOrOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated and view.action in ["retrieve", "update"]:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        return obj.customer.user == request.user


class IsAdminOrCreateOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated and request.method == "create":
            return True

        return False
