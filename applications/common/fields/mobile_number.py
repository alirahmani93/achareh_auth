from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _


class MobileNumber(models.CharField):
    def __init__(self, *args, db_collation=None, **kwargs):
        super(MobileNumber, self).__init__(*args, **kwargs)
        self.db_collation = db_collation
        self.verbose_name = _("mobile number")
        self._unique = True
        self.max_length = 13
        self.validators.append(validators.MaxLengthValidator(13))

    def to_python(self, value):
        if isinstance(value, str) or value is None:
            return value
        return str(value)
