from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ('is_approved', 'is_active')
        fields = ['id', 'first_name', 'last_name', 'username', 'mobile', 'password', 'is_approved', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class ChangePasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['current_password', 'new_password', 'confirm_password']
