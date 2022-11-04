from django.contrib.auth.models import AbstractUser
from django.db import models

from .utils import set_confirmation_code

USER_ROLE_CHOICES = (
    ("user", "user"),
    ("moderator", "moderator"),
    ("admin", "admin"),
    ("superuser", "superuser"),
)


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        verbose_name="email",
        help_text="User's email",
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )
    bio = models.TextField(
        max_length=2048,
        blank=True,
        verbose_name="Bio",
        help_text="User's bio",
    )
    role = models.CharField(
        max_length=16,
        verbose_name="Role",
        help_text="User's role",
        choices=USER_ROLE_CHOICES,
        default="user"
    )
    confirmation_code = models.CharField(
        max_length=16,
        unique=True,
        default=set_confirmation_code,
        verbose_name="confirmation_code",
        help_text="Confirmation code"
    )

    class Meta(AbstractUser.Meta):
        ordering = ("-id",)
        constraints = (
            models.UniqueConstraint(
                fields=("email", "username"),
                name="email_username_uniqueness_constraint"
            ),
            models.CheckConstraint(
                check=~models.Q(username="me"),
                name="username_<me>_is_prohibited"
            ),
        )
