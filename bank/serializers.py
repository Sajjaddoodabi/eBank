from rest_framework import serializers

from bank.models import TransactionType, TransactionDestinationUser, TransactionWay


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
    transaction_destination = serializers.CharField(source='user.get_full_name()', read_only=True)

    class Meta:
        model = TransactionDestinationUser
        read_only_fields = ('is_active', 'is_valid')
        fields = ['id', 'transaction_destination', 'destination_name', 'card_number', 'is_active', 'is_valid']


class TransactionDestinationChangeActivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionDestinationUser
        fields = ['is_active']


class TransactionDestinationChangeValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionDestinationUser
        fields = ['is_valid']


class TransactionSerializer(serializers.ModelSerializer):
    destination_user = TransactionDestinationUserSerializer(read_only=True)
    transaction_type = TransactionTypeSerializer(read_only=True)

    class Meta:
        model = TransactionDestinationUser
        read_only_fields = ('is_done', 'is_fail', 'reference_number', 'created_at', 'done_at')
        fields = ['id', 'user', 'destination_user', 'transaction_type', 'amount', 'reference_number', 'created_at',
                  'done_at', 'is_done', 'is_fail']
