from rest_framework import serializers

from bank_account.models import AccountType, Account, Card
from users.serializers import UserSerializer


class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        read_only_fields = ('is_active',)
        fields = ['id', 'title', 'is_active']


class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    account_type = AccountTypeSerializer(read_only=True)

    class Meta:
        model = Account
        read_only_fields = ('balance', 'is_active', 'is_approved')
        fields = ['id', 'user', 'account_type', 'balance', 'is_active', 'is_approved']


class CardSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)

    class Meta:
        model = Card
        read_only_fields = ('is_active', 'is_ban')
        fields = ['id', 'account', 'card_number', 'cvv2', 'created_date', 'expire_date', 'is_active', 'is_ban']
