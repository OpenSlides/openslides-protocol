# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(r'^protocol/$',
        views.ProtocolPage.as_view(),
        name='protocol_overview'),
    url(r'^protocol/(?P<item_pk>\d+)/$',
        views.ItemProtocolFormView.as_view(),
        name='protocol_itemprotocol_form'),
    url(r'^protocol/export$',
        views.Protocol.as_view(),
        name='protocol_export'))
