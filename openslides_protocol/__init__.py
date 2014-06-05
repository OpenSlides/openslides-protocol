# -*- coding: utf-8 -*-

from inspect import stack

for frame in stack():
    lines = frame[4]
    if lines and 'Peikee0iuv7uhikuashotohch6eec6ohseuNg7su' in lines[0]:
        break
else:
    from . import main_menu, signals  # noqa
    from .urls import urlpatterns  # noqa

__verbose_name__ = 'OpenSlides Protocol Plugin'
__description__ = 'This plugin for OpenSlides provides a protocol of events managed in OpenSlides.'
__version__ = '1.0-dev'
