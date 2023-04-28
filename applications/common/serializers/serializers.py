from rest_framework.fields import BooleanField, CharField

from applications.common.models import Configuration
from applications.common.serializers.base import BaseSerializer, BaseModelSerializer


class HealthSerializer(BaseSerializer):
    app_name = CharField(max_length=256)
    version = CharField(max_length=100)
    app = BooleanField()
    database = BooleanField()
    redis = BooleanField()


class ConfigurationSerializers(BaseModelSerializer):
    class Meta:
        model = Configuration
        fields = [
            'app_name',
            'app_version',
            'maintenance_mode',
            'server_time_zone',
            'server_time',
        ]
