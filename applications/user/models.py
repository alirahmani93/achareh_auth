from django.contrib.auth.models import AbstractUser
from django.core.cache import cache
from django.db import models
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from applications import get_now
from applications.common.fields.mobile_number import MobileNumber


class User(AbstractUser):
    mobile_number = MobileNumber()

    USERNAME_FIELD = 'mobile_number'

    def __str__(self):
        return self.mobile_number

    @classmethod
    def register_user(cls, mobile_number):
        return cls.objects.create(mobile_number=mobile_number, username=mobile_number)

    def get_token(self):
        if self.is_authenticated:
            refresh = RefreshToken.for_user(self)
        else:
            return {}
        token = {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
        return token


