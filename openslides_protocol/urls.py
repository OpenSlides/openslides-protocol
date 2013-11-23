# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns

from . import views

urlpatterns = patterns(
    '',
    url(r'^(?P<item_pk>\d+)/$',
        views.ItemProtocolFormView.as_view(),
        name='protocol_itemprotocol_form'),
    url(r'^$',
        views.ProtocolPage.as_view(),
        name='protocol_protocol_page'))
