from django.core.cache import cache
from django.test import TestCase
from rest_framework.reverse import reverse

from applications.user.models import User


class AuthTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.all().delete()
        cache.clear()
        pass

    def test_exists(self):
        response = self.client.post(reverse('auth-exist'), data={'mobile_number': "09123456789"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'code': 'OK',
            'data': {'link': '/api/auth/otp/verify/'},
            'detail': 'OK',
            'error': None
        })
        User.objects.create(mobile_number='09123456788')

        response = self.client.post(reverse('auth-exist'), data={'mobile_number': "09123456788"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'code': 'OK',
            'data': {'link': '/api/auth/login/'},
            'detail': 'OK',
            'error': None
        })

    def test_otp_verify(self):
        # Fail OTP
        response = self.client.post(reverse('auth-otp-verify'),
                                    data={'mobile_number': "09123456789", 'otp': '1'})
        self.assertEqual(response.status_code, 400)
        r = response.json()
        self.assertEqual(r, {'code': 'otp_expired', 'data': {}, 'detail': 'Otp expired', 'error': None})

        # success OTP
        self.client.post(reverse('auth-exist'), data={'mobile_number': "09123456789"})
        otp = int(cache.get('09123456789'))
        self.assertTrue(otp)
        self.assertEqual(int, type(otp))
        cache.set('09123456789', otp, 100)
        response = self.client.post(reverse('auth-otp-verify'),
                                    data={'mobile_number': "09123456789", 'otp': otp})
        self.assertEqual(response.status_code, 201)
        r = response.json()
        self.assertEqual(r, {
            'detail': 'Created',
            'code': 'created',
            'error': None,
            'data': {
                'link': '/api/auth/register/',
                'tokens': {
                    'access': r['data']['tokens']['access'],
                    'refresh': r['data']['tokens']['refresh']
                },
            }
        })
        response = self.client.post(
            reverse('auth-register'),
            data={"password": "123", "first_name": "ali", "last_name": "rahmani", "email": "ali@2test.com"})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'code': 'forbidden', 'data': {}, 'detail': 'Forbidden', 'error': None})

    def test_login(self):
        user = User.objects.create(mobile_number='09123456788', first_name='ali', last_name='rahmani',
                                   email='ali@test.com')
        user.set_password('123')
        user.save()
        response = self.client.post(reverse('auth-exist'), data={'mobile_number': "09123456788"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'code': 'OK',
            'data': {'link': '/api/auth/login/'},
            'detail': 'OK',
            'error': None
        })

        response = self.client.post(reverse('auth-login'), data={'mobile_number': "09123456788", 'password': '123'})
        self.assertEqual(response.status_code, 200)
        r = response.json()
        self.assertEqual(
            r,
            {
                'detail': 'OK', 'code': 'OK', 'error': None,
                'data': {
                    'id': 1, 'username': '', 'mobile_number': '09123456788',
                    'first_name': 'ali', 'last_name': 'rahmani',
                    'tokens': {
                        'access': r['data']['tokens']['access'],
                        'refresh': r['data']['tokens']['refresh']
                    }
                }
            }
        )
        response = self.client.post(reverse('auth-login'), data={'mobile_number': "09123456788", 'password': '1234'})
        self.assertEqual(response.status_code, 403)
        r = response.json()
        self.assertEqual(
            r,
            {'code': 'login_failed', 'data': {}, 'detail': 'Login failed', 'error': None}
        )
        self.client.post(reverse('auth-login'), data={'mobile_number': "09123456788", 'password': '1234'})
        self.client.post(reverse('auth-login'), data={'mobile_number': "09123456788", 'password': '1234'})
        self.client.post(reverse('auth-login'), data={'mobile_number': "09123456788", 'password': '1234'})

        response = self.client.post(reverse('auth-login'), data={'mobile_number': "09123456788", 'password': '12345'})
        self.assertEqual(response.status_code, 403)
        r = response.json()
        self.assertEqual(
            r,
            {'code': 'ip_blocked', 'data': {}, 'detail': 'This IP blocked', 'error': ''}
        )
