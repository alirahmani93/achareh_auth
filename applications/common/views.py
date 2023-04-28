import abc
import logging

from django.conf import settings
from django.db import connections
from django_redis import get_redis_connection
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from applications.common.models import Configuration
from applications.common.serializers.serializers import HealthSerializer, ConfigurationSerializers
from applications.common.utils.response import custom_response
from applications.common.utils.time import get_now, standard_response_datetime


class BaseViewSet(viewsets.GenericViewSet, abc.ABC):
    serializer_classes: dict = {}
    pagination_class = None
    input_serializer = None

    def get_queryset(self):
        return self.queryset.filter(is_active=True)

    def data_validation(self, serializer=None):
        ser = serializer if serializer else self.serializer_class
        serializer_ = ser(data=self.request.data)
        serializer_.is_valid(raise_exception=True)
        return serializer_, serializer_.validated_data

    def get_serializer_class(self):
        version = '' if self.request.version is None else self.request.version
        if self.action in self.serializer_classes:
            return self.serializer_classes[self.action][version] if version in self.serializer_classes[self.action] \
                else self.serializer_classes[self.action][list(self.serializer_classes[self.action].keys())[-1]]
        return self.serializer_class

    def response_paginated_query(self, queryset):
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    class Meta:
        abstract = True


class BaseAPIView(APIView, abc.ABC):
    queryset = None
    serializer_class = None

    def get_queryset(self):
        return self.queryset.filter(is_active=True)

    def data_validation(self):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return serializer, serializer.validated_data


class AppViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = ConfigurationSerializers

    def list(self, request, *args, **kwargs):
        """Return data what Non-sensitive information. """
        data: dict = Configuration.load()
        result = self.serializer_class(data).data
        result['server_time'] = standard_response_datetime(get_now())
        return custom_response(data=result)

    @action(methods=['GET'], detail=False, url_path='time', url_name='time')
    def time(self, request, *args, **kwargs):
        return custom_response(data={'time': standard_response_datetime(get_now())})

    @action(methods=['GET'], detail=False, url_path='ping', url_name='ping', permission_classes=(IsAuthenticated,))
    def ping(self, request, *args, **kwargs):
        return custom_response(data={'detail': 'PONG'})

    @action(methods=['GET'], detail=False, url_path='health', url_name='health', serializer_class=HealthSerializer)
    def health(self, request, *args, **kwargs):

        def app():
            app = 1
            return app

        def database():
            # Postgres
            postgres = 0
            try:
                db_conn = connections['default']
                db_conn.cursor()
                postgres = 1
            except:
                logging.error(msg={"postgres": "Postgres Server not available"})
                print(">>>", "Postgres not available")

            if postgres:
                return 1
            else:
                return 0

        def redis():
            status = 0

            try:
                redis_check = get_redis_connection()
                if redis_check:
                    status = 1
                    return status
                return status
            except:
                logging.error(msg={"redis": "redis Server not available"})
                print(">>>", "redis Server not available")

                return status

        return custom_response(data=HealthSerializer({
            "app_name": settings.PROJECT_NAME,
            'version': settings.VERSION,
            'app': app(),
            'database': database(),
            'redis': redis(),
        }).data)
