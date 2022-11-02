import os

from django.conf import settings


def set_confirmation_code(size=settings.CONFIRMATION_CODE_BYTE_SIZE):
    return os.urandom(size).hex()
