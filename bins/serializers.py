from uuid import uuid4
from random import randint
from rest_framework import serializers

from .models import BinModel, BinLocationModel

class AddBinSerializer(serializers.Serializer):
    location_id = serializers.IntegerField()
    emptied_at = serializers.DateTimeField()
    bin_image = serializers.FileField()


class BinSerializer(serializers.ModelSerializer):
    class Meta:
        model = BinModel
        fields = ("location", "bin_url", "emptied_at", "uploaded_by")
    

    def create(self, validated_data):
        validated_data["id"] = uuid4()
        return super().create(validated_data)
    

class BinLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BinLocationModel
        fields = ("location","city","state","capacity", "longitude","latitude")

    def validate(self, attrs):
        attrs["location"] = attrs["location"].capitalize().strip()
        attrs["city"] = attrs["city"].capitalize().strip()
        attrs["state"] = attrs["state"].strip().capitalize()

        return attrs
    
    def create(self, validated_data):
        validated_data["id"] = randint(90, 569125)
        return super().create(validated_data)