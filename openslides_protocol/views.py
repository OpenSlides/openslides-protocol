from openslides.utils.auth import has_perm
from openslides.utils.rest_api import ModelViewSet

from .access_permissions import ItemProtocolAccessPermissions
from .models import ItemProtocol


class ItemProtocolViewSet(ModelViewSet):
    """
    API endpoint for ItemProtocols.
    """
    access_permissions = ItemProtocolAccessPermissions()
    queryset = ItemProtocol.objects.all()

    def check_view_permissions(self):
        return has_perm(self.request.user, 'openslides_protocol.can_write_protocol')
