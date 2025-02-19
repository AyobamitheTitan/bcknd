from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class UserModel(models.Model):
    id = models.UUIDField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(unique=True, max_length=15)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"User [ id: {self.id}, email: {self.email}]"