# -*- coding: utf-8 -*-

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver

from openslides.core.signals import post_database_setup
from openslides.participant.models import Group


@receiver(post_database_setup, dispatch_uid='openslides_protocol_add_permission')
def openslides_protocol_add_permission(sender, **kwargs):
    """
    Adds the protocol permission the the builtin staff group.
    """
    try:
        group_staff = Group.objects.get(name='Staff', pk=4)
    except Group.DoesNotExist:
        # Do not add the protocol permission
        pass
    else:
        ct_openslides_protocol = ContentType.objects.get(app_label='openslides_protocol', model='itemprotocol')
        protocol_perm = Permission.objects.get(content_type=ct_openslides_protocol, codename='can_write_protocol')
        group_staff.permissions.add(protocol_perm)
