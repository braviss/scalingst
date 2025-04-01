from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timedelta
from django.utils.timezone import now
import random
import string

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_premium = models.BooleanField(default=False)
    premium_since = models.DateTimeField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default='default-avatar.png')
    is_email_verified = models.BooleanField(default=False)
    my_invite_code = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        verbose_name="My Invite Code"
    )

    def __str__(self):
        return self.username



class EmailVerificationCode(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="email_verification")
    code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return self.created_at + timedelta(minutes=10) < now()

    @staticmethod
    def generate_code():
        return ''.join(random.choices(string.digits, k=6))