import os

from django.apps import AppConfig
from openslides.utils.collection import Collection

from . import __description__, __verbose_name__, __version__


class ProtocolAppConfig(AppConfig):
    name = 'openslides_protocol'
    verbose_name = __verbose_name__
    description = __description__
    version = __version__
    angular_site_module = True
    js_files = [
        'static/js/openslides_protocol/base.js',
        'static/js/openslides_protocol/site.js',
        'static/js/openslides_protocol/templatehooks.js',
        'static/js/openslides_protocol/templates.js',  # This file has a different basefolder!
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            import settings
        except ImportError:
            # When testing, we cannot import settings here..
            pass
        else:
            # Add the staticfiles dir to OpenSlides
            base_path = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))
            # remove the app folder 'openslides_protcol'
            base_path = os.path.dirname(base_path)
            settings.STATICFILES_DIRS.append(os.path.join(base_path, 'static'))

    def ready(self):
        # Import all required stuff.
        from openslides.core.signals import post_permission_creation
        from openslides.utils.rest_api import router
        from .signals import add_permissions_to_builtin_groups
        from .views import ObjectProtocolViewSet, ProtocolViewSet

        # Connect signals.
        post_permission_creation.connect(
            add_permissions_to_builtin_groups,
            dispatch_uid='protocol_add_permissions_to_builtin_groups'
        )

        # Register viewsets.
        router.register(self.get_model('ObjectProtocol').get_collection_string(), ObjectProtocolViewSet)
        router.register(self.get_model('Protocol').get_collection_string(), ProtocolViewSet)

    def get_startup_elements(self):
        yield Collection(self.get_model('ObjectProtocol').get_collection_string())
        yield Collection(self.get_model('Protocol').get_collection_string())
