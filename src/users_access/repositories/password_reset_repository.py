from django.db import models, transaction
import logging

logger = logging.getLogger('django')


class PasswordResetManager(models.Manager):
    def create_password_reset(self, user):
        try:
            with transaction.atomic():
                password_reset, created = self.get_or_create(
                    user=user,
                    defaults={
                        'reset_counter': 1
                    }
                )

                if not created:
                    password_reset.reset_counter = models.F('reset_counter') + 1
                    password_reset.save(update_fields=['reset_counter', 'updated_at'])
                logger.info(
                    f"Password reset record {'created' if created else 'updated'}: "
                    f"ID={password_reset.id}, user={user.email}, reset_counter={password_reset.reset_counter}"
                )
            return password_reset
        except KeyError as e:
            logger.error(f"Missing required field: {e} for user {user.email}")
            return None
        except Exception as e:
            logger.error(f"Error while creating password reset for user {user.email}: {e}")
        return None
