import random

from django.conf import settings
from django.core.cache import cache
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import User
from .serializers import UserSerializer, UserExistSerializer, LoginSerializer, OtpVerifySerializer, \
    UserRegisterSerializer
from .. import OTP_EXPIRED_400, UNAUTHORIZED_401, CREATED_201, LOGIN_FAILED_403
from ..common.utils.ip_address import IPBlock
from ..common.utils.response import custom_response
from ..common.views import BaseViewSet


class AuthViewSet(BaseViewSet):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    OPT_EXPIRE_TIME = settings.OPT_EXPIRE_TIME

    def otp_send(self, mobile_number: str) -> int:
        """Generate OTP and send SMS."""
        otp = random.randint(100000, 999999)
        cache.set(mobile_number, otp, self.OPT_EXPIRE_TIME)
        print(otp)
        return otp

    @staticmethod
    def otp_check(mobile_number, otp) -> bool:
        return True if cache.get(mobile_number) == otp else False

    @action(detail=False, methods=['POST'], url_path='exist', url_name='exist',
            serializer_class=UserExistSerializer)
    def exist(self, request, *args, **kwargs):
        serializer, valid_data = self.data_validation(serializer=self.input_serializer)
        mobile_number = valid_data['mobile_number']
        is_exist = User.objects.filter(mobile_number=mobile_number).exists()

        if is_exist:
            return custom_response(data={"link": reverse('auth-login')}, )
        self.otp_send(mobile_number=mobile_number)
        return custom_response(data={"link": reverse('auth-otp-verify')})

    @action(detail=False, methods=['POST'], url_path='otp/verify', url_name='otp-verify',
            serializer_class=OtpVerifySerializer)
    def otp_verify(self, request, *args, **kwargs):
        serializer, valid_data = self.data_validation()
        mobile_number = valid_data['mobile_number']
        otp = valid_data['otp']
        if self.otp_check(mobile_number=mobile_number, otp=otp):
            user = User.register_user(mobile_number=valid_data['mobile_number'])
            return custom_response(data={"link": reverse('auth-register'),
                                         'tokens': user.get_token()
                                         }, status_code=CREATED_201)
        IPBlock.attempt(request=request, mobile_number=mobile_number)
        return custom_response(status_code=OTP_EXPIRED_400)

    @action(detail=False, methods=['POST'], url_path='register', url_name='register',
            serializer_class=UserRegisterSerializer)
    def register(self, request, *args, **kwargs):
        serializer, valid_data = self.data_validation()

        # get User
        if not self.request.auth:
            return custom_response(status_code=UNAUTHORIZED_401)

        user = self.request.user

        # update user
        user.first_name = valid_data['first_name']
        user.last_name = valid_data['last_name']
        user.email = valid_data['email']

        # set password
        user.set_password(valid_data['password'])
        user.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'], url_path='login', url_name='login',
            serializer_class=LoginSerializer)
    def login(self, request, *args, **kwargs):
        serializer, valid_data = self.data_validation()
        mobile_number = valid_data['mobile_number']

        # find user
        failed_attempt_msg = {'detail': "username/password wrong"}
        try:
            user = User.objects.get(mobile_number=mobile_number)
        except User.DoesNotExist:
            IPBlock.attempt(request=request, mobile_number=mobile_number)
            return custom_response(data={}, status_code=LOGIN_FAILED_403)

        # check password
        if not user.check_password(valid_data['password']):
            IPBlock.attempt(request=request, mobile_number=mobile_number)
            return custom_response(data={}, status_code=LOGIN_FAILED_403)

        return custom_response(data=UserSerializer(user).data)
