import os

from django.utils.crypto import get_random_string


def random_string(length=0) -> str:
    if length <= 0:
        length = os.getenv('RANDOM_STRING_LENGTH', 6)
    return get_random_string(length)
