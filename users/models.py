from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    mobile = models.CharField(max_length=11)
    birth_date = models.DateField(default=timezone.now)
    address = models.CharField(max_length=200, blank=True, null=True)
    national_code = models.CharField(max_length=20, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        if self.get_full_name() != ' ':
            return self.get_full_name()
        return self.username
