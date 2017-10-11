from django.db.utils import IntegrityError
from openslides.utils.auth import has_perm
from openslides.utils.rest_api import (
    DestroyModelMixin,
    GenericViewSet,
    ListModelMixin,
    ModelViewSet,
    Response,
    RetrieveModelMixin,
    UpdateModelMixin,
    ValidationError,
)
from rest_framework import status

from .access_permissions import (
    ObjectProtocolAccessPermissions,
    ProtocolAccessPermissions,
)
from .models import ObjectProtocol, Protocol


class ObjectProtocolViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    """
    API endpoint for ObjectProtocols.
    """
    access_permissions = ObjectProtocolAccessPermissions()
    queryset = ObjectProtocol.objects.all()

    def check_view_permissions(self):
        return has_perm(self.request.user, 'openslides_protocol.can_write_protocol')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except IntegrityError:
            content_object = serializer.data['content_object']
            raise ValidationError('The protocol for "{}" with id {} exists already.'.format(
                content_object['collection'],
                content_object['id']))

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProtocolViewSet(ModelViewSet):
    """
    API endpoint for Protocols.
    """
    access_permissions = ProtocolAccessPermissions()
    queryset = Protocol.objects.all()

    def check_view_permissions(self):
        return (has_perm(self.request.user, 'openslides_protocol.can_write_protocol') and
                self.request.user.is_authenticated())

    def perform_create(self, serializer):
        """
        Customized method to inject the request.user into serializer's save
        method so that the request.user can be saved into the model field.
        """
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        """
        Customized method to ensure that every user can change only his own
        personal notes.
        """
        if self.get_object().user != self.request.user:
            self.permission_denied(request)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Customized method to ensure that every user can delete only his own
        personal notes.
        """
        if self.get_object().user != self.request.user:
            self.permission_denied(request)
        return super().destroy(request, *args, **kwargs)
