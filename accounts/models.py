from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        FINANCE_MANAGER = 'FINANCE', 'Finance Manager'

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.FINANCE_MANAGER,
    )

    def is_admin(self):
        return self.role == self.Role.ADMIN