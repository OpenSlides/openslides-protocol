from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from openslides.users.models import Group


def add_permissions_to_builtin_groups(sender, **kwargs):
    """
    Adds the protocol permission the the builtin staff group.
    """
    try:
        group_staff = Group.objects.get(name='Staff')
        group_admin = Group.objects.get(name='Admin')
    except Group.DoesNotExist:
        # Do not add the protocol permission
        pass
    else:
        perm = Permission.objects.get(
            content_type=ContentType.objects.get(
                app_label='openslides_protocol',
                model='objectprotocol'),
            codename='can_write_protocol')
        group_staff.permissions.add(perm)
        group_admin.permissions.add(perm)
