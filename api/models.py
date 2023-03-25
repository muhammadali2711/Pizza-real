from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password, **extra_fields):

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(phone, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=128, unique=False, blank=True, null=True)
    phone = models.CharField(max_length=15, unique=True, null=False, blank=False)
    name = models.CharField(max_length=15, blank=True, null=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone


class ServerTokens(models.Model):
    key = models.CharField(max_length=256)
    token = models.CharField(max_length=2000)

    def __str__(self):
        return self.key


class OTP(models.Model):
    key = models.CharField(max_length=256)
    phone = models.CharField(max_length=25)
    tries = models.IntegerField(default=0)
    is_expired = models.BooleanField(default=False)
    state = models.CharField(max_length=128, default="step_one")
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False, editable=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

