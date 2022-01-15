from rest_framework import serializers
from .models import BaseUserProfile
from django.db import IntegrityError
from rest_framework import fields

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
            raise Exception('User with this email already exits.')

class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True, min_length=8)
    new_password = serializers.CharField(
        write_only=True, required=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = BaseUserProfile
        fields = ('old_password', 'new_password', 'confirm_password')

    def validate(self, data):
        
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Password fields didn't match.")
        return data

    def validate_old_password(self, value):
        user = self.context['user']
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"})
        return value

class ForgotPasswordSerializer(serializers.ModelSerializer):

    new_password = serializers.CharField(min_length=8, write_only=True)
    confirm_new_password = serializers.CharField(min_length=8, write_only=True)
    
    class Meta:
        model = BaseUserProfile
        fields = ('new_password', 'confirm_new_password')

        def validate(self, data):
            if data['new_password'] != data['confirm_new_password']:
                raise serializers.ValidationError("Password fields didn't match.")
            return data