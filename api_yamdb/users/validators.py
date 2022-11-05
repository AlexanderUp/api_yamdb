from django.core.exceptions import ValidationError


def me_username_validator(value):
    if value == "me":
        raise ValidationError("Username <me> is prohibited.")
