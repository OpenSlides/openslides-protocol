from openslides.utils.access_permissions import BaseAccessPermissions
from openslides.utils.auth import has_perm


class ItemProtocolAccessPermissions(BaseAccessPermissions):
    """
    Access permissions for ItemProtocol and the ViewSet.
    """
    def check_permissions(self, user):
        return has_perm(user, 'openslides_protocol.can_write_protocol')

    def get_serializer_class(self, user=None):
        from .serializers import ItemProtocolSerializer

        return ItemProtocolSerializer
