from django.core.exceptions import PermissionDenied

from rest_framework import permissions

from inventory.devices.models import Device


class OwnerRequiredMixin:
    """
    Mixin used to ensure that the request user is the owner of the profile or account they are attempting to modify.

    Method:
    - get_object(queryset=None): Retrieves the object from the database based on the provided queryset and checks if
      the request user is the owner of the object. Raises PermissionDenied if not.

    Raises:
        PermissionDenied: If the request user is not authenticated or is not the owner of the object.
    """

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)

        if not self.request.user.is_authenticated or obj.account != self.request.user:
            raise PermissionDenied

        return obj


class IsBusinessOwner(permissions.BasePermission):
    """
    Custom permission class used to verify that the current user is the owner of the business associated with
    the device for CRUD operations.

    Methods:
    - has_permission(request, view): Determines if the request should be permitted based on whether the request user
      is the owner of the business. Retrieves business ID from request data or, if missing, from device details based
      on view's kwargs.

    Returns:
        bool: True if the user is the owner of the business; otherwise, False.

    Raises:
        ValueError: If the business ID in the request is not a valid integer (implied by returning False).
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

        return is_owner
