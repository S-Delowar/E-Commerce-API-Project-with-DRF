from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
        Custom permission to ensure only the owner of a CartItem can access or modify it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user