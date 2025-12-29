from django.db import transaction
from django.conf import settings
from users_access.models.notification import Notification


class NotificationRepository:
    """Repository for Notification write operations."""

    @staticmethod
    def create_notification(user, notification_type: str, title: str, message: str,
                           priority: str = 'medium', related_entity_type: str = None,
                           related_entity_id: str = None, metadata: dict = None):
        """Create a new notification."""
        with transaction.atomic():
            notification = Notification.objects.create(
                user=user,
                notification_type=notification_type,
                title=title,
                message=message,
                priority=priority,
                related_entity_type=related_entity_type,
                related_entity_id=related_entity_id,
                metadata=metadata
            )
            notification.full_clean()
            notification.save()
            return notification

    @staticmethod
    def mark_as_read(notification):
        """Mark a notification as read."""
        from django.utils import timezone
        with transaction.atomic():
            notification.is_read = True
            notification.read_at = timezone.now()
            notification.full_clean()
            notification.save()
            return notification

    @staticmethod
    def mark_all_as_read(user):
        """Mark all notifications for a user as read."""
        from django.utils import timezone
        with transaction.atomic():
            Notification.objects.filter(user=user, is_read=False).update(
                is_read=True,
                read_at=timezone.now()
            )

    @staticmethod
    def delete_notification(notification):
        """Delete a notification."""
        with transaction.atomic():
            notification.delete()

