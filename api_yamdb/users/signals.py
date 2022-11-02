from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


@receiver(post_save, sender=User)
def send_confirmation_code(sender, instance, created, **kwargs):
    if created:
        send_mail(
            "Confirmation code",
            f"Your confirmation code is {instance.confirmation_code}.",
            "admin@example.com",
            [instance.email],
        )
