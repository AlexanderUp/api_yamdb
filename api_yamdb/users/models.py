from django.contrib.auth.models import AbstractUser
from django.db import models

USER_ROLE_CHOICES = (
    ("USER", "user"),
    ("MODERATOR", "moderator"),
    ("ADMIN", "admin"),
    ("SUPERUSER", "superuser"),
)


class User(AbstractUser):
    bio = models.TextField(
        verbose_name="Bio",
        help_text="User's bio",
        blank=True,
    )
    role = models.CharField(
        max_length=16,
        verbose_name="Role",
        help_text="User's role",
        choices=USER_ROLE_CHOICES,
        default="USER",
    )
