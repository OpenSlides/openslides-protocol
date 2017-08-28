from django.db import models
from openslides.agenda.models import Item
from openslides.utils.models import RESTModelMixin

from .access_permissions import ItemProtocolAccessPermissions


class ItemProtocol(RESTModelMixin, models.Model):
    """
    Model for a protocol entry for an agenda item.
    """
    access_permissions = ItemProtocolAccessPermissions()

    item = models.OneToOneField(Item)

    protocol = models.TextField(blank=True)

    class Meta:
        default_permissions = ()
        permissions = (('can_write_protocol', 'Can write protocol'),)
