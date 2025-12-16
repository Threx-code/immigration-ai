from rest_framework.permissions import IsAuthenticated
from .base_api import BaseAPI
from helpers import fields as input_fields
from django_filters.rest_framework import DjangoFilterBackend


class AuthAPI(BaseAPI):
    permission_classes = [IsAuthenticated]
    field = input_fields
    filter_backends = [DjangoFilterBackend]



