import logging
import random
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils.timezone import timedelta
from django.utils.translation import gettext_lazy as _

from .utils.handler import get_version, get_app_name
from .utils.time import get_now, standard_timestamp_response
from .utils.validator import version_regex


class BaseModel(models.Model):
    """All models in project inherit. These parameters are necessary. """
    uuid = models.UUIDField(verbose_name=_("UUID"), editable=False, default=uuid4)
    is_active = models.BooleanField(verbose_name=_("Is active"), default=True)
    updated_time = models.DateTimeField(verbose_name=_("Updated time"), auto_now=True)
    created_time = models.DateTimeField(verbose_name=_("Created time"), auto_now_add=True)

    def __str__(self):
        return f"{self.uuid}"

    class Meta:
        abstract = True


class SingletonBaseModel(BaseModel):
    """Used to ensure that a class can only have one concurrent instance."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.__class__.objects.count() == 1:
                raise Exception(_('Only one instance of configurations is allowed.'))
            self.created_time = get_now()
        super().save(*args, **kwargs)


class Configuration(SingletonBaseModel):
    """
        System configuration have some data are use in other entity and specifications.
    properties return static data at project
    """

    app_name = models.CharField(verbose_name=_("App Name"), max_length=255, default=get_app_name)
    app_version = models.CharField(
        verbose_name=_("App Version"), max_length=100, default=get_version, validators=[version_regex])
    maintenance_mode = models.BooleanField(verbose_name=_('Maintenance mode'), default=False)

    @property
    def server_time_zone(self):
        return settings.TIME_ZONE

    @property
    def server_time(self):
        return standard_timestamp_response(get_now())

    def __str__(self):
        return f"{self.app_name} ( {self.app_version} )"

    class Meta:
        verbose_name = _("Configuration")
        verbose_name_plural = _("Configurations")

    @classmethod
    def load(cls):
        data, _ = cls.objects.get_or_create()
        return data

