from users_access.repositories.user_repository import UserRepository
from users_access.selectors.user_selector import UserSelector
import logging

logger = logging.getLogger('django')


class UserService:

    @staticmethod
    def create_user(email, password, first_name, last_name):
        try:
            return UserRepository.create_user(email, password, first_name, last_name)
        except Exception as e:
            logger.error(f"Error creating user {email}: {e}")
            return None

    @staticmethod
    def create_superuser(email, password, first_name, last_name):
        try:
            return UserRepository.create_superuser(email, password, first_name, last_name)
        except Exception as e:
            logger.error(f"Error creating superuser {email}: {e}")
            return None

    @staticmethod
    def update_user(user, **fields):
        try:
            return UserRepository.update_user(user, **fields)
        except Exception as e:
            logger.error(f"Error updating user {user.email}: {e}")
            return None

    @staticmethod
    def update_avatar(user, avatar):
        try:
            return UserRepository.update_avatar(user, avatar)
        except Exception as e:
            logger.error(f"Error updating avatar for user {user.email}: {e}")
            return None

    @staticmethod
    def remove_avatar(user):
        try:
            return UserRepository.remove_avatar(user)
        except Exception as e:
            logger.error(f"Error removing avatar for user {user.email}: {e}")
            return None

    @staticmethod
    def update_names(user, first_name=None, last_name=None):
        try:
            return UserRepository.update_names(user, first_name, last_name)
        except Exception as e:
            logger.error(f"Error updating names for user {user.email}: {e}")
            return None

    @staticmethod
    def activate_user(user):
        try:
            return UserRepository.activate_user(user)
        except Exception as e:
            logger.error(f"Error activating user {user.email}: {e}")
            return None

    @staticmethod
    def update_password(user, password):
        try:
            return UserRepository.update_password(user, password)
        except Exception as e:
            logger.error(f"Error updating password for user {user.email}: {e}")
            return None

    @staticmethod
    def is_verified(user):
        try:
            return UserRepository.is_verified(user)
        except Exception as e:
            logger.error(f"Error verifying user {user.email}: {e}")
            return None

    @staticmethod
    def get_all():
        try:
            return UserSelector.get_all()
        except Exception as e:
            logger.error(f"Error fetching all users: {e}")
            return []

    @staticmethod
    def email_exists(email):
        try:
            return UserSelector.email_exists(email)
        except Exception as e:
            logger.error(f"Error checking if email exists: {e}")
            return False

    @staticmethod
    def get_by_email(email):
        try:
            return UserSelector.get_by_email(email)
        except Exception as e:
            logger.error(f"Error fetching user by email {email}: {e}")
            return None

