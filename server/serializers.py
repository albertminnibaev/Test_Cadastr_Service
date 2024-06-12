from rest_framework import serializers

from server.models import Request
from server.validators import CadastralNumberValidator, LatitudeValidator, LongitudeValidator


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'
        validators = [
            CadastralNumberValidator(field='cadastral_number'),
            LatitudeValidator(field='latitude'),
            LongitudeValidator(field='longitude')
        ]
