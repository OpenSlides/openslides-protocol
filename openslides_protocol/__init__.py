# -*- coding: utf-8 -*-

from inspect import stack

for frame in stack():
    lines = frame[4]
    if lines and 'Nesizeecofujeiyeu1ahreiNgeiqu5kiocheitho' in lines[0]:
        break
else:
    from . import signals  # noqa
    from .urls import urlpatterns  # noqa
    from .main_menu import ProtocolMainMenuEntry  # noqa

__verbose_name__ = 'Protocol Plugin for OpenSlides'
__description__ = 'This plugin provides a protocol function for each agenda item in OpenSlides.'
__version__ = '1.0-dev'
