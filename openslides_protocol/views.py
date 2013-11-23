# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

from openslides.agenda.models import Item
from openslides.utils.template import Tab
from openslides.utils.views import TemplateView, UpdateView

from .forms import ItemProtocolForm
from .models import ItemProtocol


class ItemProtocolFormView(UpdateView):
    """
    View for a protocol chapter for an agenda item.
    """
    form_class = ItemProtocolForm
    permission_required = 'openslides_protocol.can_write_protocol'

    def dispatch(self, *args, **kwargs):
        """
        Override: Retrieves the agenda item from the pk number given in the url and
        inserts it as self.item before continueing the view.
        """
        self.item = get_object_or_404(Item, pk=kwargs['item_pk'])
        return super(ItemProtocolFormView, self).dispatch(*args, **kwargs)

    def get_object(self, *args, **kwargs):
        """
        Returns the item protocol model instance witch belongs to the agenda
        item. Creates a new instance if necessary.
        """
        obj, __ = ItemProtocol.objects.get_or_create(item=self.item)
        return obj


class ProtocolPage(TemplateView):
    """
    View with the link to download the final protocol.
    """
    template_name = 'openslides_protocol/protocol_page.html'
    permission_required = 'openslides_protocol.can_write_protocol'

    def get_context_data(self, *args, **kwargs):
        """
        Inserts all agenda items into the context.
        """
        context = super(ProtocolPage, self).get_context_data(*args, **kwargs)
        context['items'] = Item.objects.all()
        return context


def register_tab(request):
    """
    Registers the protocol menu entry.
    """
    return Tab(
        title=_('Protocol'),
        app='openslides_protocol',
        url=reverse('protocol_protocol_page'),
        permission=request.user.has_perm('openslides_protocol.can_write_protocol'),
        selected=request.path.startswith('/openslides_protocol/'))
