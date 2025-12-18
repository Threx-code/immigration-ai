from django.db import transaction
from django.utils import timezone
from users_access.models import UserDeviceSession


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
            return device_session

    @staticmethod
    def revoke_session(session):
        with transaction.atomic():
            session.revoked = True
            session.save(update_fields=["revoked"])
            return True

    @staticmethod
    def revoke_all_for_user(user):
        with transaction.atomic():
            UserDeviceSession.objects.filter(user=user, revoked_at__isnull=True).update(
                revoked_at=timezone.now(), revoked=True
            )
            UserDeviceSession.objects.filter(user=user, revoked=False).update(revoked=True)
            return True

    @staticmethod
    def mark_active(session):
        with transaction.atomic():
            session.last_active = timezone.now()
            session.save(update_fields=["last_active"])
            return True
