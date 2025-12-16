from django.db import models, transaction
from django.utils import timezone
import logging

logger = logging.getLogger("django")


class UserDeviceSessionManager(models.Manager):
    """
    Manager for UserDeviceSession.
    """
    def create_device_session(self, user, fingerprint, ip_address, user_agent, device_info, session_id, last_active):
        with transaction.atomic():
            device_session = self.create(
                user=user,
                fingerprint=fingerprint,
                ip_address=ip_address,
                user_agent=user_agent,
                device_info=device_info,
                session_id=session_id,
                last_active=last_active
            )

            device_session.full_clean()
            logger.info(f"Device session created for user {user.id} with session ID {device_session.session_id}")
            return device_session

    def active_sessions_for_user(self, user):
        return self.filter(user=user, revoked=False, revoked_at__isnull=True).order_by("-last_active")

    def get_by_session_id(self, session_id, fingerprint=None):
        try:
            qs = self.filter(session_id=session_id, revoked=False, revoked_at__isnull=True)
            if fingerprint:
                qs = qs.filter(fingerprint=fingerprint)
            return qs.first()
        except Exception as e:
            logger.exception(f"Error fetching session {session_id}: {e}")
            return None

    def revoke_session(self, session_id):
        try:
            session = self.filter(session_id=session_id, revoked=False, revoked_at__isnull=True).first()
            if session:
                session.revoked = True
                session.save(update_fields=["revoked"])
                logger.info(f"Session {session_id} revoked")
                return True
            return False
        except Exception as e:
            logger.exception(f"Error revoking session {session_id}: {e}")
            return False

    def revoke_all_for_user(self, user):
        try:
            self.filter(user=user, revoked_at__isnull=True).update(revoked_at=timezone.now(), revoked=True)
            self.filter(user=user, revoked=False).update(revoked=True)
            logger.info(f"Revoked all sessions for user {user.id}")
            return True
        except Exception as e:
            logger.exception(f"Error revoking all sessions for user {user.id}: {e}")
            return False

    def mark_active(self, session_id):
        try:
            session = self.filter(session_id=session_id, revoked=False).first()
            if session:
                session.last_active = timezone.now()
                session.save(update_fields=["last_active"])
                return True
            return False
        except Exception as e:
            logger.exception(f"Error marking session {session_id} active: {e}")
            return False
