from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from rest_framework.exceptions import ValidationError
import uuid


def validate_photo_size(photo):
    max_size = 5 * 1024 * 1024  # 5 MB
    if photo.size > max_size:
        raise ValidationError("Photo size should not exceed 5MB.")
    return photo


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, password, **extra_fields)


HAIR_TYPE_CHOICES = [
    ('Oily', 'Oily'),
    ('Dry', 'Dry'),
    ('Normal', 'Normal'),
    ('Wavy', 'Wavy'),
]

SHAMPOO_ROUTINE_CHOICES = [
    ('Daily', 'Daily'),
    ('Every other day', 'Every other day'),
    ('Twice a week', 'Twice a week'),
    ('Weekly', 'Weekly'),
]


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=30, blank=True)
    photo = models.ImageField(
        upload_to="user_photos/",
        validators=[validate_photo_size],
        blank=True,
        null=True
    )
    hair_type = models.CharField(max_length=50, blank=True, choices=HAIR_TYPE_CHOICES)
    shampoo_routine = models.CharField(max_length=50, blank=True, choices=SHAMPOO_ROUTINE_CHOICES)
    date_joined = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.full_name or self.email

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super().save(*args, **kwargs)
