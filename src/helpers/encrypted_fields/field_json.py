import json
from encrypted_model_fields.fields import EncryptedTextField


class EncryptedJSONField(EncryptedTextField):

    def from_db_value(self, value, expression=None, connection=None):
        if value is None:
            return None
        try:
            return json.loads(super().from_db_value(value, expression, connection))
        except (json.JSONDecodeError, TypeError):
            return None

    def to_python(self, value):
        if value is None or isinstance(value, dict):
            return value
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return None

    def get_prep_value(self, value):
        if value is None:
            return None
        if isinstance(value, dict):
            return super().get_prep_value(json.dumps(value))
        return super().get_prep_value(value)