from openslides.utils.rest_api import ModelSerializer
from openslides.utils.validate import validate_html

from .models import ItemProtocol


class ItemProtocolSerializer(ModelSerializer):
    """
    Serializer for openslides_protocol.models.ItemProtocol object.
    """
    class Meta:
        model = ItemProtocol
        fields = (
            'id',
            'item',
            'protocol',
        )

    def validate(self, data):
        if 'protocol' in data:
            data['protocol'] = validate_html(data['protocol'])
        return data
