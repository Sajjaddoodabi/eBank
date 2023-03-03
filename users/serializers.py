from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ('is_approved', 'is_active')
        fields = ['id', 'first_name', 'last_name', 'mobile', 'password', 'is_approved', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True}
        }
