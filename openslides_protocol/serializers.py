from django.core.exceptions import ObjectDoesNotExist
from openslides.utils.collection import get_model_from_collection_string
from openslides.utils.rest_api import (
    JSONField,
    ModelSerializer,
    ValidationError,
)
from openslides.utils.validate import validate_html

from .models import ObjectProtocol, Protocol


class ContentObjectSerializer(JSONField):
    def to_representation(self, value):
        """
        Returns info concerning the related object extracted from the api URL
        of this object.
        """
        value = {'collection': value.get_collection_string(), 'id': value.get_rest_pk()}
        return super().to_representation(value)

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if not isinstance(data, dict):
            raise ValidationError('content_object has to be a dict.')
        if data.get('collection') is None or data.get('id') is None:
            raise ValidationError('collection and id has to be given.')
        try:
            data['id'] = int(data['id'])
        except TypeError:
            raise ValidationError('id has to be an int.')

        if not isinstance(data['collection'], str):
            raise ValidationError('collection has to be a string.')

        try:
            model = get_model_from_collection_string(data['collection'])
        except ValueError:
            raise ValidationError('Collection string "{}" is not valid.'.format(data['collection']))
        try:
            element = model.objects.get(pk=data['id'])
        except ObjectDoesNotExist:
            raise ValidationError('Id {} does not exist.'.format(data['id']))
        return element


class ObjectProtocolSerializer(ModelSerializer):
    """
    Serializer for openslides_protocol.models.ObjectProtocol object.
    """
    content_object = ContentObjectSerializer()

    class Meta:
        model = ObjectProtocol
        fields = (
            'id',
            'content_object',
            'protocol',
        )

    def validate(self, data):
        if 'protocol' in data:
            data['protocol'] = validate_html(data['protocol'])
        return data


class ProtocolSerializer(ModelSerializer):
    """
    Serializer for openslides_protocol.models.Protocol object.
    """
    protocol = JSONField()

    class Meta:
        model = Protocol
        fields = (
            'id',
            'protocol',
        )
