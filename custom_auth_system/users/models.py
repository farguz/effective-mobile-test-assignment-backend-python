from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class Role(models.Model):
    name = models.CharField(
        max_length=80,
        unique=True,
        verbose_name='Role name'
        )

    def __str__(self):
        return self.name
    

class Resource(models.Model):
    name = models.CharField(
        max_length=80,
        unique=True,
        verbose_name='Resource name'
        )

    def __str__(self):
        return self.name
    

class Permission(models.Model):
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='permissions'
        )
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        related_name='permissions'
        )
    can_read = models.BooleanField(default=False)
    can_create = models.BooleanField(default=False)
    can_update = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_soft_delete = models.BooleanField(default=False)

    class Meta:
        unique_together = ['role', 'resource']

    def __str__(self):
        return f'{self.role}: {self.resource}'


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
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
        )
    updated_at = models.DateTimeField(auto_now=True)

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