from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class AttemptException(APIException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail = _('Too many Attempt')
    default_code = 'too_many_attempt'
