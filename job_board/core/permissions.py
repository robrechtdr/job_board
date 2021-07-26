from rest_framework import permissions


class IsProfessional(permissions.BasePermission):

    def has_permission(self, request, view):
        # Not using user.is_professional as not available to anonymous users.
        if hasattr(request.user, 'professional') or request.user.is_staff:
            return True


class IsBusiness(permissions.BasePermission):

    def has_permission(self, request, view):
        if hasattr(request.user, 'business') or request.user.is_staff:
            return True
