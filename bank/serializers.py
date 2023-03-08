from rest_framework import serializers

from bank.models import TransactionType, TransactionDestinationUser, TransactionWay, Transaction
from bank_account.serializers import AccountSerializer
from users.serializers import UserMiniSerializer


class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        read_only_fields = ('is_active',)
        fields = ['id', 'title', 'is_active']


class TransactionTypeChangeActivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = ['is_active']


class TransactionWaySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionWay
        read_only_fields = ('is_active',)
        fields = ['id', 'title', 'is_active']


class TransactionWayChangeActivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionWay
        fields = ['is_active']


class TransactionDestinationUserSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = TransactionDestinationUser
        read_only_fields = ('is_active', 'is_valid')
        fields = ['id', 'user', 'destination_name', 'card_number', 'is_active', 'is_valid']


class TransactionDestinationChangeActivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionDestinationUser
        fields = ['is_active']


class TransactionDestinationChangeValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionDestinationUser
        fields = ['is_valid']


class TransactionSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True)
    transaction_to = TransactionDestinationUserSerializer(read_only=True)
    type = TransactionTypeSerializer(read_only=True)

    class Meta:
        model = Transaction
        read_only_fields = ('is_done', 'is_fail', 'reference_number', 'created_at', 'finish_at')
        fields = ['id', 'user', 'transaction_to', 'type', 'amount', 'reference_number', 'created_at',
                  'finish_at', 'is_done', 'is_fail']


# class TransactionChangeDoneSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Transaction
#         fields = ['is_done']
#
#
# class TransactionChangeFailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Transaction
#         fields = ['is_fail']
