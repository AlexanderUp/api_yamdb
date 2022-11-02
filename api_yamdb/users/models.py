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
        default="USER",
    )

    class Meta(AbstractUser.Meta):
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
