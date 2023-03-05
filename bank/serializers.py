from rest_framework import serializers

from bank.models import TransactionType, TransactionDestinationUser, TransactionWay
from users.serializers import UserSerializer


class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        read_only_fields = ('is_active',)
        fields = ['id', 'title', 'is_active']


class TransactionWaySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionWay
        read_only_fields = ('is_active',)
        fields = ['id', 'title', 'is_active']


class TransactionDestinationUserSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.get_full_name()')

    class Meta:
        model = TransactionDestinationUser
        read_only_fields = ('is_active', 'is_valid')
        fields = ['id', 'user', 'destination_user', 'card_number', 'is_active', 'is_valid']


class TransactionSerializer(serializers.ModelSerializer):
    destination_user = TransactionDestinationUserSerializer(read_only=True)
    transaction_type = TransactionTypeSerializer(read_only=True)

    class Meta:
        model = TransactionDestinationUser
        read_only_fields = ('is_done', 'is_fail', 'reference_number', 'created_at', 'done_at')
        fields = ['id', 'user', 'destination_user', 'transaction_type', 'amount', 'reference_number', 'created_at',
                  'done_at', 'is_done', 'is_fail']