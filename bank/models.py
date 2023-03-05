from django.db import models

from users.models import User


class TransactionType(models.Model):
    title = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class TransactionWay(models.Model):
    title = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class TransactionDestinationUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name='transaction_destination')
    destination_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=19, unique=True)
    is_active = models.BooleanField(default=False)
    is_valid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.destination_user} - {self.card_number}'


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user')
    transaction_to = models.ForeignKey(TransactionDestinationUser, on_delete=models.DO_NOTHING, related_name='destination_user')
    type = models.ForeignKey(TransactionType, on_delete=models.RESTRICT, related_name='transaction_type')
    amount = models.PositiveIntegerField(default=0)
    reference_number = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    done_at = models.DateTimeField()
    is_done = models.BooleanField(default=False)
    is_fail = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.type} - {self.amount}'
