from abc import ABC
from helpers import fields as input_fields
from django.conf import settings
from helpers.request.client import Client

class ExternalRequest(ABC):

    def __init__(self, endpoint: str):
        self.headers = {
            input_fields.ACCEPT: input_fields.APPLICATION_JSON,
            input_fields.CONTENT_TYPE: input_fields.APPLICATION_JSON,
            input_fields.MONO_SEC_KEY: getattr(settings, input_fields.SANDBOX_SECRET_KEY),
        }
        self.client = Client(getattr(settings, input_fields.MONO_BASE_URL))
        self.endpoint = endpoint