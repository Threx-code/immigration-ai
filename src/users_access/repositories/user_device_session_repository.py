from django.db import transaction
from django.utils import timezone
from users_access.models import UserDeviceSession
import logging

logger = logging.getLogger("django")


class UserDeviceSessionRepository:

    @staticmethod
    def create_device_session(user, fingerprint, ip_address, user_agent, device_info, session_id, last_active):
        with transaction.atomic():
            device_session = UserDeviceSession(
                user=user,
                fingerprint=fingerprint,
                ip_address=ip_address,
                user_agent=user_agent,
                device_info=device_info,
                session_id=session_id,
                last_active=last_active
            )
            device_session.full_clean()
            device_session.save()
            logger.info(f"Device session created for user {user.id} with session ID {session_id}")
            return device_session

    @staticmethod
    def revoke_session(session):
        with transaction.atomic():
            session.revoked = True
            session.save(update_fields=["revoked"])
            logger.info(f"Session {session.session_id} revoked")
            return True

    @staticmethod
    def revoke_all_for_user(user):
        with transaction.atomic():
            UserDeviceSession.objects.filter(user=user, revoked_at__isnull=True).update(
                revoked_at=timezone.now(), revoked=True
            )
            UserDeviceSession.objects.filter(user=user, revoked=False).update(revoked=True)
            logger.info(f"Revoked all sessions for user {user.id}")
            return True

    @staticmethod
    def mark_active(session):
        with transaction.atomic():
            session.last_active = timezone.now()
            session.save(update_fields=["last_active"])
            return True
