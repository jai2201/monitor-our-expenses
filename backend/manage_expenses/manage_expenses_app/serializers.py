from rest_framework import serializers
from .models import BaseUserProfile


class CustomUserCreateSerializser(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password =  serializers.CharField(min_length=8, write_only=True)


    class Meta:
        model = BaseUserProfile
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}