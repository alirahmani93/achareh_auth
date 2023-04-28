import json

from django.test import TestCase

from applications.common.models import  Configuration
from applications.user.models import User


class BaseTestCase(TestCase):

    def setUp(self, empty=False) -> None:
        super(BaseTestCase, self).setUp()
        self.config, _ = Configuration.objects.get_or_create()
        self.response = None
        self.decoded: dict = {}

    def _check_status_code(self, status_code: dict):
        self.assertEqual(self.response.status_code, status_code.get('number'))

    def _check_code(self, status_code: dict):
        self.assertEqual(self.decoded['code'], status_code['code'])

    def _check_detail(self, status_code: dict):
        self.assertEqual(self.decoded['detail'], status_code['detail'])

    def _check_data(self, mock_data: dict):
        self.assertEqual(self.decoded['data'], mock_data)

    def check_response_status_code(self, status_code: dict):
        self._check_status_code(status_code=status_code)
        self.decoded = json.loads(self.response.content.decode())
        self._check_code(status_code=status_code)
        self._check_detail(status_code=status_code)

        return True

    def check_response(self, mock_data: dict):
        self._check_data(mock_data=mock_data)

        return True

    def clean(self):
        self.decoded = {}
        self.response = None

    def tearDown(self) -> None:
        super().tearDown()
        self.clean()
