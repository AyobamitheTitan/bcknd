from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class UserModel(AbstractBaseUser):
    id = models.UUIDField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(unique=True, max_length=15)
    password = models.CharField(max_length=150)
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text=(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        # validators=[username_validator],   
    )

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "username"

    def __str__(self):
        return f"User [ id: {self.id}, email: {self.email}]"