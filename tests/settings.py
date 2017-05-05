#
# Settings file for tests only
#

from openslides.global_settings import *  # noqa

DEBUG = False

SECRET_KEY = 'secret'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

INSTALLED_PLUGINS += (  # noqa
    'openslides_protocol',)

INSTALLED_APPS += INSTALLED_PLUGINS  # noqa

TIME_ZONE = 'Europe/Berlin'

# Use a faster passwort hasher
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Use the dummy cache that does not cache anything
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
    },
    'locmem': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
    }
}
