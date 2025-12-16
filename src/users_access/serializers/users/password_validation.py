from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from helpers import fields as input_fields
import re

class PasswordValidation:

    def __init__(self, password: str, email: str):
        self.password = password
        self.email = email


    def validate(self):
        try:
            validate_password(self.password)
            if any(part.lower() in self.password.lower() for part in self.email.split('@')[0].split('.')):
                raise serializers.ValidationError(input_fields.PASSWORD_CANNOT_BE_PART_OF_YOUR_EMAIL)
            if re.search(input_fields.NUMBER_REGEX, self.password) is None:
                raise serializers.ValidationError(input_fields.PASSWORD_MUST_CONTAIN_A_NUMBER)
            if re.search(input_fields.UPPERCASE_REGEX, self.password) is None:
                raise serializers.ValidationError(input_fields.PASSWORD_MUST_CONTAIN_A_UPPERCASE)
            if re.search(input_fields.LOWERCASE_REGEX, self.password) is None:
                raise serializers.ValidationError(input_fields.PASSWORD_MUST_CONTAIN_A_LOWERCASE)
            if re.search(input_fields.SPECIAL_CHARACTERS, self.password):
                raise serializers.ValidationError(input_fields.PASSWORD_MUST_CONTAIN_A_SPECIAL_CHARACTER)
        except serializers.ValidationError as e:
            raise serializers.ValidationError({input_fields.PASSWORD: e.detail})
        return self.password
