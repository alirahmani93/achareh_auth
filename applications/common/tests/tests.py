from django.conf import settings
from django.core.cache import cache
from rest_framework.reverse import reverse

from applications import OK_200
from applications.common.models import Configuration
from applications.common.tests.tests_base import BaseTestCase


class CommonBaseTestCase(BaseTestCase):
    def setUp(self, empty=False) -> None:
        super(CommonBaseTestCase, self).setUp(empty=empty)
        Configuration.objects.all().delete()


class CommonTestCase(CommonBaseTestCase):
    def setUp(self, empty=False) -> None:
        super(CommonTestCase, self).setUp(empty=False)
        cache.clear()
        self.configuration, _ = Configuration.objects.get_or_create()

    def test_app_config(self):
        self.response = self.client.get(reverse('app-list'))
        self.check_response_status_code(status_code=OK_200)
        mock_data = {
            'app_name': settings.PROJECT_NAME, 'app_version': settings.VERSION, 'maintenance_mode': False,
            'server_time_zone': 'UTC', 'server_time': self.decoded['data']['server_time'],
        }
        self.check_response(mock_data=mock_data)

    def test_health(self):
        self.response = self.client.get(reverse('app-health'))
        self.assertEqual(
            self.response.json(),
            {
                'detail': 'OK', 'code': 'OK', 'error': None,
                'data': {
                    'app_name': settings.PROJECT_NAME,
                    'version': settings.VERSION,
                    'app': True,
                    'database': True,
                    'redis': True
                }}
        )
