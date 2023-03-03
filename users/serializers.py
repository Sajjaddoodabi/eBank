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


class UserFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ('is_approved', 'is_active')
        fields = ['id', 'first_name', 'last_name', 'username', 'mobile', 'national_code', 'address', 'postal_code',
                  'is_approved', 'is_active']


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ('is_approved', 'is_active')
        fields = ['id', 'first_name', 'last_name', 'username', 'mobile', 'is_approved', 'is_active']


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


class ResetPasswordSerializer(serializers.ModelSerializer):
    confirm_code = serializers.CharField(
        required=True,
        write_only=True,
    )

    class Meta:
        model = User
        fields = ['confirm_code']
