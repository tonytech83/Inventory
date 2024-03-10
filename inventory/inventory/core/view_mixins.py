from django.core.exceptions import PermissionDenied


class OwnerRequiredMixin:
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)

        if not self.request.user.is_authenticated or obj.account != self.request.user:
            raise PermissionDenied

        return obj
