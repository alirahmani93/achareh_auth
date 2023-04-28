from django.core.cache import cache
from rest_framework import serializers

from .models import User
from .. import BaseSerializer


class UserSerializer(serializers.ModelSerializer):
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'mobile_number', 'first_name', 'last_name', 'tokens']

    @staticmethod
    def get_tokens(obj):
        return obj.get_token()


class UserExistSerializer(BaseSerializer):
    mobile_number = serializers.CharField()


class LoginSerializer(UserExistSerializer):
    password = serializers.CharField()

    def validate(self, attrs):
        from rest_framework.validators import ValidationError
        if cache.get(f"mobile_number_blocked_{attrs['mobile_number']}"):
            raise ValidationError("mobile_number_blocked")
        return super(LoginSerializer, self).validate(attrs)


class OtpVerifySerializer(UserExistSerializer):
    otp = serializers.IntegerField()


class UserRegisterSerializer(BaseSerializer):
    password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
