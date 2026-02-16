from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone', 'avatar', 'plan', 'plan_expires_at',
            'total_bots', 'total_messages', 'created_at'
        ]
        read_only_fields = ['id', 'total_bots', 'total_messages', 'created_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Ro'yxatdan o'tish uchun"""
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Parollar mos kelmadi!")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """Login uchun"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)