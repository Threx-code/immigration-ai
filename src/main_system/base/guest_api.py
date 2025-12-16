from rest_framework.permissions import AllowAny
from .base_api import BaseAPI

class GuestAPI(BaseAPI):
    permission_classes = (AllowAny,)




