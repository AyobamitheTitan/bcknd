from uuid import uuid4
from rest_framework import serializers
from rest_framework.exceptions import (
    AuthenticationFailed, 
    NotFound, 
    ValidationError
)
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q

from .models import UserModel

class LoginSerializer(serializers.Serializer):
    email_or_phone_number = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)

    def validate(self, attrs):
        email_or_phone = attrs.get("email_or_phone_number")
        password = attrs.get("password")

        if email_or_phone and password:
            user = UserModel.objects.filter(Q(email=email_or_phone)| Q(phone_number=email_or_phone)).first()
            if not user:
                raise NotFound(detail="User not found")
            if not check_password(password, user.password):
                raise AuthenticationFailed(detail="Incorrect password")
            
            attrs['user'] = user
            return attrs
        else:
            raise ValidationError(detail="Please provide email/phone_number and password")




class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50, write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = UserModel
        fields = ("first_name","last_name","email","password","phone_number")

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)
        validated_data["id"] = uuid4()
        return UserModel.objects.create(**validated_data)