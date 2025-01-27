from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'phone', 'email', 'is_2fa_enabled']

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomUser
        fields = ['name', 'phone', 'email', 'password']

    def create(self, validated_data):
        return CustomUser.objects.create_user(
            name=validated_data['name'],
            phone=validated_data['phone'],
            password=validated_data['password'],
            email=validated_data.get('email', None),
        )

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(phone=data['phone'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid phone or password.")
        if not user.is_active:
            raise serializers.ValidationError("Account is disabled.")
        return user

class TwoFAVerifySerializer(serializers.Serializer):
    otp = serializers.CharField()

    def validate(self, data):
        return data
