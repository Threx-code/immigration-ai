from typing import Optional
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager
from django.db import transaction
from users_access.models.user import User
from helpers import fields as input_fields
import logging

logger = logging.getLogger('django')


class UserRepository:

    @staticmethod
    def create_user(email, password, first_name, last_name):
        with transaction.atomic():
            normalized_email = BaseUserManager.normalize_email(email)
            user = User.objects.create(
                email=normalized_email,
                first_name=first_name,
                last_name=last_name,
                role=input_fields.USER
            )

            user.set_password(password)
            user.is_active = True
            user.is_staff = False
            user.is_superuser = False
            user.save(using=User.objects._db)
            user.full_clean()
            return user

    @staticmethod
    def create_superuser(email, password, first_name, last_name):
        user = UserRepository.create_user(email, password, first_name, last_name)
        user.role = input_fields.ADMIN
        user.is_superuser = True
        user.is_staff = True
        user.full_clean()
        user.save()
        return user

    @staticmethod
    def update_user(user, **fields):
        with transaction.atomic():
            for key, value in fields.items():
                setattr(user, key, value)
            user.save(using=User.objects._db)
            user.full_clean()
            return user

    @staticmethod
    def update_avatar(user, avatar):
        with transaction.atomic():
            old_avatar = user.avatar
            user.avatar = avatar
            user.full_clean()
            user.save()
            if old_avatar and old_avatar.name and old_avatar.name != user.avatar.name:
                old_avatar.delete(save=False)
            return user

    @staticmethod
    def remove_avatar(user):
        with transaction.atomic():
            old_avatar = user.avatar
            user.avatar = None
            user.full_clean()
            user.save()
            if old_avatar and old_avatar.name:
                old_avatar.delete(save=False)
            return user

    @staticmethod
    def update_names(user, first_name: Optional[str], last_name: Optional[str]):
        with transaction.atomic():
            user.first_name = first_name if first_name else user.first_name
            user.last_name = last_name if last_name else user.last_name
            user.full_clean()
            user.save()
            return user

    @staticmethod
    def activate_user(user):
        with transaction.atomic():
            user.is_verified = True
            user.full_clean()
            user.save()
            return user

    @staticmethod
    def update_password(user, password):
        with transaction.atomic():
            user.password = make_password(password)
            user.full_clean()
            user.save()
            return user

    @staticmethod
    def is_verified(user):
        with transaction.atomic():
            user.is_verified = True
            user.full_clean()
            user.save()
            return user
