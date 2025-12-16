from rest_framework import serializers
from django.contrib.auth import authenticate
from helpers import fields as input_fields
from users_access.services.user_service import UserService


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={input_fields.INPUT_TYPE: input_fields.PASSWORD}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get(input_fields.EMAIL).lower()
        password = attrs.get(input_fields.PASSWORD)
        if not email or not password:
            raise serializers.ValidationError(input_fields.EMAIL_PASSWORD_REQUIRED)

        if UserService().email_exists(email):
            user = authenticate(self.context.get(input_fields.REQUEST), email=email, password=password)
            if not user:
                raise serializers.ValidationError(input_fields.INVALID_CREDENTIALS)
            if not user.is_active:
                raise serializers.ValidationError(input_fields.USER_NOT_ACTIVE)
            if not user.is_verified:
                raise serializers.ValidationError(input_fields.EMAIL_NOT_VERIFIED)
            attrs[input_fields.USER] = user
        else:
            raise serializers.ValidationError(input_fields.INVALID_CREDENTIALS)

        return attrs


class TwoFactorVerifySerializer(serializers.Serializer):
    otp = serializers.CharField(min_length=6, max_length=6)
    is_2fa = serializers.BooleanField(default=False)


