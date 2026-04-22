from django.core.exceptions import PermissionDenied


class UserIsOwnerMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if obj.owner != request.user:
            raise PermissionDenied("You are not the owner")

        return super().dispatch(request, *args, **kwargs)