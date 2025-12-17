from django.db import transaction, models
from users_access.models import PasswordReset
import logging

logger = logging.getLogger('django')


class PasswordResetRepository:

    @staticmethod
    def create_password_reset(user):
        with transaction.atomic():
            password_reset, created = PasswordReset.objects.get_or_create(
                user=user,
                defaults={'reset_counter': 1}
            )

            if not created:
                password_reset.reset_counter = models.F('reset_counter') + 1
                password_reset.save(update_fields=['reset_counter', 'updated_at'])

            password_reset.refresh_from_db()
            logger.info(
                f"Password reset record {'created' if created else 'updated'}: "
                f"ID={password_reset.id}, user={user.email}, reset_counter={password_reset.reset_counter}"
            )
            return password_reset
