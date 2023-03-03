from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    mobile = models.CharField(max_length=11)
    address = models.CharField(max_length=200)
    national_code = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=20)
    is_approved = models.BooleanField(default=False)

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        if self.get_full_name:
            return self.get_full_name
        return self.username
