from uuid import uuid4
from rest_framework.serializers import ModelSerializer

from .models import BinModel

class BinSerializer(ModelSerializer):

    class Meta:
        model = BinModel
        fields = ("location","fill_level")

    
    def create(self, validated_data):
        validated_data["id"] = uuid4()
        return super().create(validated_data)