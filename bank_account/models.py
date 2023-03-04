from django.db import models

from users.models import User


class AccountType(models.Model):
    title = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    type = models.ForeignKey(AccountType, on_delete=models.RESTRICT, related_name='account_type')
    balance = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} - {self.type}'


class Card(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='card')
    card_number = models.CharField(max_length=16)
    cvv2 = models.CharField(max_length=4)
    created_date = models.DateField(auto_now_add=True)
    expire_date = models.DateField()
    is_active = models.BooleanField(default=False)
    is_ban = models.BooleanField(default=False)

    def __str__(self):
        return self.account.user
