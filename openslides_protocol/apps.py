from django.apps import AppConfig
from openslides.utils.collection import Collection

from . import (
    __description__,
    __license__,
    __url__,
    __verbose_name__,
    __version__,
)


class ProtocolAppConfig(AppConfig):
    name = 'openslides_protocol'
    verbose_name = __verbose_name__
    description = __description__
    version = __version__
    license = __license__
    url = __url__
    angular_site_module = True
    js_files = [
        'static/js/openslides_protocol/base.js',
        'static/js/openslides_protocol/site.js',
        'static/js/openslides_protocol/templatehooks.js',
        'static/js/openslides_protocol/templates.js'
    ]

    def ready(self):
        # Import all required stuff.
        from openslides.core.config import config
        from openslides.core.signals import post_permission_creation
        from openslides.utils.rest_api import router
        from .config_variables import get_config_variables
        from .signals import add_permissions_to_builtin_groups
        from .views import ObjectProtocolViewSet, ProtocolViewSet

        # Define config variables
        config.update_config_variables(get_config_variables())

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
