# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy

from openslides.utils.main_menu import MainMenuEntry


class ProtocolMainMenuEntry(MainMenuEntry):
    verbose_name = ugettext_lazy('Protocol')
    required_permission = 'openslides_protocol.can_write_protocol'
    default_weight = 200
    pattern_name = 'protocol_overview'
    icon_css_class = 'icon-star'
    #stylesheets = ['css/protocol.css']
