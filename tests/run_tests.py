# -*- coding: utf-8 -*-

import sys
import os

from openslides.__main__ import main as openslides_main
from openslides.utils.main import setup_django_settings_module


def main():
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    setup_django_settings_module(os.path.join(os.path.dirname(__file__), 'settings.py'))
    sys.argv.insert(1, 'django')
    sys.argv.insert(2, 'test')
    return openslides_main()


if __name__ == '__main__':
    main()
