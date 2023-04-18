from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """User uchun qo'shimcha telefon nomer modeli"""
    phone = models.CharField(max_length=20, blank=True, null=True)
    kpi_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"

