from django.db.models.signals import post_save
from django.dispatch import receiver
from data_ingestion.models.rule_validation_task import RuleValidationTask
from users_access.services.notification_service import NotificationService
from users_access.tasks.email_tasks import send_rule_validation_task_email_task
import logging

logger = logging.getLogger('django')


@receiver(post_save, sender=RuleValidationTask)
def handle_rule_validation_task_created(sender, instance, created, **kwargs):
    """
    Signal handler for rule validation task creation.
    - Sends notification to assigned reviewer/admin
    - Sends email notification
    """
    if created and instance.assigned_to:
        # New validation task assigned
        NotificationService.create_notification(
            user_id=str(instance.assigned_to.id),
            notification_type='rule_validation_task',
            title='New Rule Validation Task',
            message=f'A new rule validation task has been assigned to you.',
            priority='medium',
            related_entity_type='rule_validation_task',
            related_entity_id=str(instance.id),
            metadata={
                'parsed_rule_id': str(instance.parsed_rule.id) if instance.parsed_rule else None,
                'status': instance.status
            }
        )
        
        # Send email notification
        send_rule_validation_task_email_task.delay(
            reviewer_id=str(instance.assigned_to.id),
            task_id=str(instance.id)
        )

