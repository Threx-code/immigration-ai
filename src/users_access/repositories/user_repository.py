from typing import Optional
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager
from django.db import IntegrityError
from helpers import fields as input_fields
import logging

logger = logging.getLogger('django')


class UserManager(BaseUserManager):

    def create_user(self, email, password, first_name, last_name):
        try:
            user = self.model(
                email=self.normalize_email(email),
                first_name=first_name,
                last_name=last_name,
                role=input_fields.USER
            )

            user.set_password(password)
            user.is_active = True
            user.is_staff = False
            user.is_superuser = False
            user.save(using=self._db)
            return user
        except IntegrityError as e:
            logger.error(f"Integrity error while creating user {email}: {e}")
        except Exception as e:
            logger.error(f"Error while creating user {email}: {e}")
        return None


    def create_superuser(self, email: str, password: str, first_name, last_name):
        try:
            user = self.create_user(email, password, first_name, last_name)
            user.role = input_fields.ADMIN
            user.is_superuser = True
            user.is_staff = True
            user.save(using=self._db)
            return user
        except Exception as e:
            logger.error(f"Error while creating superuser {email}: {e}")
        return None


    def update_user(self, user, **fields):
        try:
            for key, value in fields.items():
                setattr(user, key, value)
            user.save(using=self._db)
            return user
        except Exception as e:
            logger.error(f"Error while updating user {user.email}: {e}")
        return None

    def update_avatar(self, user, avatar):
        try:
            user.avatar = avatar
            user.save(using=self._db)
            return user
        except Exception as e:
            logger.error(f"Error while updating avatar for user {user.email}: {e}")
        return None


    def update_names(self, user, first_name: Optional[str], last_name: Optional[str]):
        try:
            user.first_name = first_name if first_name else user.first_name
            user.last_name = last_name if last_name else user.last_name
            user.save(using=self._db)
            return user
        except Exception as e:
            logger.error(f"Error while updating full name for user {user.email}: {e}")
        return None


    def activate_user(self, user):
        try:
            user.is_verified = True
            user.save(using=self._db)
            return user
        except Exception as e:
            logger.error(f"Error while activating user {user.email}: {e}")
        return None


    def update_password(self, user, password):
        try:
            user.password = make_password(password)
            user.save(using=self._db)
            return user
        except Exception as e:
            logger.error(f"Error while updating password for user {user.email}: {e}")
        return None


    def connect_bvn(self, user, bvn):
        try:
            user.bvn = bvn
            user.save(using=self._db)
            return user
        except Exception as e:
            logger.error(f"Error while connecting BVN for user {user.email}: {e}")
        return None


    def is_verified(self, user):
        try:
            user.is_verified = True
            user.save(using=self._db)
            return user
        except Exception as e:
            logger.error(f"Error while verifying user {user.email}: {e}")
        return None


    def get_all(self):
        try:
            return self.get_queryset().all()
        except Exception as e:
            logger.error(f"Error while getting all users: {e}")
            return []

    def email_exists(self, email: str) -> bool:
        try:
            return self.get_queryset().filter(email__iexact=email).exists()
        except Exception as e:
            logger.error(f"Error while checking if email exists: {e}")
            return False

    def get_by_email(self, email: str):
        try:
            return self.get_queryset().get(email__iexact=email)
        except Exception as e:
            logger.error(f"Error while getting user with email {email}: {e}")
        return None





