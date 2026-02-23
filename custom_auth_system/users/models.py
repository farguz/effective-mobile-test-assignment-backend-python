from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField(
        max_length=150,
        blank=False
        )
    middle_name = models.CharField(
        max_length=150,
        blank=False
        )
    last_name = models.CharField(
        max_length=150,
        blank=False
        )
    email = models.EmailField(
        unique=True,
        blank=False
        )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'middle_name', 'last_name', ]

    def get_full_name(self):
        """
        extends original func with middle_name
        """
        full_name = f'{self.last_name} {self.middle_name} {self.first_name}'
        return full_name.strip()

    def __str__(self):
        return f'{self.get_full_name()}: {self.email}'
    
    