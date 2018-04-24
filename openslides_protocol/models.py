from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from jsonfield import JSONField
from openslides.utils.models import RESTModelMixin

from .access_permissions import (
    ObjectProtocolAccessPermissions,
    ProtocolAccessPermissions,
)


class ObjectProtocolManager(models.Manager):
    """
    Customized model manager for prefetching content objects.
    """
    def get_full_queryset(self):
        """
        Returns the normal queryset with all objectProtocols. In the background all
        related items are prefetched from the database.
        """
        return self.get_queryset().prefetch_related('content_object')


class ObjectProtocol(RESTModelMixin, models.Model):
    """
    Model for a protocol entry for an agenda item.
    """
    access_permissions = ObjectProtocolAccessPermissions()

    objects = ObjectProtocolManager()

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    object_id = models.PositiveIntegerField(null=True, blank=True)

    content_object = GenericForeignKey()

    protocol = models.TextField(blank=True)

    class Meta:
        default_permissions = ()
        permissions = (('can_write_protocol', 'Can write protocol'),)
        unique_together = ('content_type', 'object_id')


class Protocol(RESTModelMixin, models.Model):
    """
    Model for a protocol entry for an agenda item.
    """
    access_permissions = ProtocolAccessPermissions()

    protocol = JSONField(default=[])

    class Meta:
        default_permissions = ()
