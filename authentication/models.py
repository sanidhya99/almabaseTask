from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from .manage import CustomUserManager

class CustomUser(AbstractUser):
    username = None  # Remove username field
    name = models.CharField(max_length=50)
    phone = models.CharField(
        max_length=10,
        unique=True,
        blank=True,
        null=True,
        validators=[RegexValidator(regex=r"^\d{10}$", message="Phone number must be 10 digits only.")]
    )
    email = models.EmailField(null=True, blank=True, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_2fa_enabled = models.BooleanField(default=True)  # To enable/disable 2FA
    otp_secret = models.CharField(max_length=32, blank=True, null=True)  # For storing OTP secret

    objects = CustomUserManager()

    REQUIRED_FIELDS = ["name"]
    USERNAME_FIELD = 'phone'

    def __str__(self):
        return self.name
