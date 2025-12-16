from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from .password_validation import PasswordValidation
from helpers import fields as input_fields


class PasswordUpdateSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True)
    old_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        user = self.context[input_fields.REQUEST].user
        if not check_password(value, user.password):
            raise serializers.ValidationError(input_fields.INVALID_OLD_PASSWORD)


    def validate_password(self, password):
        email = self.instance.email
        return PasswordValidation(password, email).validate()

