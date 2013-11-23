# -*- coding: utf-8 -*-

from django import forms

from .models import ItemProtocol


class ItemProtocolForm(forms.ModelForm):
    """
    Form for a protocol entry for an agenda item.
    """
    class Meta:
        model = ItemProtocol
        fields = ['protocol']
