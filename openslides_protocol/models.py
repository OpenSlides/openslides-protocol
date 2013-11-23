# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy, ugettext_noop

from openslides.agenda.models import Item


class ItemProtocol(models.Model):
    """
    Model for a protocol entry for an agenda item.
    """
    item = models.OneToOneField(Item)
    protocol = models.TextField(verbose_name=ugettext_lazy('Protocol'))

    class Meta:
        permissions = (('can_write_protocol', ugettext_noop('Can write protocol entries')),)

    def __unicode__(self):
        return _('Protocol for %(item)s') % {'item': self.item}

    @models.permalink
    def get_absolute_url(self, link=None):
        """
        Returns always the url to the item protocol form view.
        """
        return ('protocol_itemprotocol_form', [str(self.pk)])
