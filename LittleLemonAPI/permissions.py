from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsManagerOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        # Everyone can read
        if request.method in SAFE_METHODS:
            return True

        # Only managers can modify
        return request.user.groups.filter(
            name='Manager'
        ).exists()

class IsManager(BasePermission):

    def has_permission(self, request, view):

        return request.user.groups.filter(
            name='Manager'
        ).exists()

class IsDeliveryCrew(BasePermission):

    def has_permission(self, request, view):

        return request.user.groups.filter(
            name='Delivery crew'
        ).exists()