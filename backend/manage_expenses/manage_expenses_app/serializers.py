from rest_framework import serializers
from .models import BaseUserProfile
from django.db import IntegrityError

class CustomUserCreateSerializser(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password =  serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = BaseUserProfile
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        try:
            user = BaseUserProfile(
                email=validated_data['email'],
                fullname=validated_data['fullname'],
                profile_picture=validated_data['profile_picture'],
            )
            user.set_password(validated_data['password'])
            user.save()
            return user
        except IntegrityError as exception:
            raise Custom409(exception)