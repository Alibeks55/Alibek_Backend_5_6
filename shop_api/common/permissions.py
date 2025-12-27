from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


class IsAnonymous(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated or not request.user.is_staff:
            return False
        if request.method == 'POST':
            return False
        return True

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff
