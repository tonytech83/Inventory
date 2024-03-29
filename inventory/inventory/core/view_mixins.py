from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import Response

from inventory.business.models import Business
from inventory.devices.models import Device


class OwnerRequiredMixin:
    """
    Used when request user tried to modify foreign profile
    """
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)

        if not self.request.user.is_authenticated or obj.account != self.request.user:
            raise PermissionDenied

        return obj


# class IsOwnerMixin:
#     """
#     Mixin to check if the current user is the owner of the business.
#     """
#
#     def check_ownership(self, business_id):
#         business = get_object_or_404(Business, id=business_id)
#         if business.owner != self.request.user:
#             # Return a Response indicating permission denied if the user is not the owner
#             return Response({"detail": "You do not have permission to perform this action."},
#                             status=status.HTTP_403_FORBIDDEN)
#         # Return None if the user is the owner
#         return None


class IsBusinessOwner(permissions.BasePermission):
    """
    Used for CRUD operations for devices
    """
    def has_permission(self, request, view):
        business_id = request.data.get('business')

        if not business_id:
            device_id = view.kwargs.get('pk')
            device = Device.objects.get(id=device_id)
            business_id = device.business.pk

            if not business_id:
                return False

        try:
            business_id = int(business_id)
        except ValueError:
            return False

        is_owner = request.user.owner.filter(id=business_id).exists()

        a = 5

        return is_owner




