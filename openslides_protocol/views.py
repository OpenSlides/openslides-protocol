# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import RequestContext, Template
from django.template.loader import get_template
from django.utils.translation import ugettext as _

from openslides.agenda.models import Item
from openslides.utils.template import Tab
from openslides.utils.views import PermissionMixin, TemplateView, UpdateView, View

from .forms import ItemProtocolForm
from .models import ItemProtocol


class ProtocolPage(TemplateView):
    """
    View with the link to all items and to the download the final protocol.
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


class ItemProtocolFormView(UpdateView):
    """
    View for a protocol entry for an agenda item.
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


class Protocol(PermissionMixin, View):
    """
    """
    permission_required = 'openslides_protocol.can_write_protocol'

    def get(self, *args, **kwargs):
        """
        Renders the protocol with the template given in the settings
        (OPENSLIDES_PROTOCOL_TEMPLATE_PATH) or the default template.
        """
        try:
            template_path = settings.OPENSLIDES_PROTOCOL_TEMPLATE_PATH
        except AttributeError:
            template = get_template('openslides_protocol/protocol.tex.tpl')
        else:
            with open(template_path) as template_file:
                template = Template(template_file.read())
        context = RequestContext(
            self.request,
            {'items': Item.objects.all()})
        response = HttpResponse(template.render(context), content_type="text/plain")
        response['Content-Disposition'] = 'attachment; filename="protocol.tex"'
        return response


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
