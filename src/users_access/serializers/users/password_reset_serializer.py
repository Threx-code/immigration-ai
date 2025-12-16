from rest_framework import serializers
from users.services.service import UserService
from helpers import fields as input_fields


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        email = email.strip().lower()
        user = UserService().get_by_email(email)
        if not user:
            raise serializers.ValidationError(input_fields.EMAIL_DOES_NOT_EXIST)

        return user