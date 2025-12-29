from django.db.models.signals import post_save
from django.dispatch import receiver
from ai_decisions.models.eligibility_result import EligibilityResult
from users_access.services.notification_service import NotificationService
from users_access.tasks.email_tasks import send_eligibility_result_email_task
from human_reviews.services.review_service import ReviewService
import logging

logger = logging.getLogger('django')


@receiver(post_save, sender=EligibilityResult)
def handle_eligibility_result_created(sender, instance, created, **kwargs):
    """
    Signal handler for eligibility result creation.
    - Sends notification to user
    - Sends email notification
    - Auto-escalates to human review if confidence < 0.6
    """
    if created:
        # Send notification to user
        NotificationService.create_notification(
            user_id=str(instance.case.user.id),
            notification_type='eligibility_result_ready',
            title=f'Eligibility Result: {instance.visa_type.name}',
            message=f'Your eligibility check for {instance.visa_type.name} is complete. Outcome: {instance.outcome}.',
            priority='high' if instance.outcome == 'eligible' else 'medium',
            related_entity_type='eligibility_result',
            related_entity_id=str(instance.id),
            metadata={
                'outcome': instance.outcome,
                'confidence': instance.confidence,
                'visa_type': str(instance.visa_type.id)
            }
        )
        
        # Send email notification (async via Celery)
        send_eligibility_result_email_task.delay(
            user_id=str(instance.case.user.id),
            eligibility_result_id=str(instance.id),
            outcome=instance.outcome,
            confidence=instance.confidence
        )
        
        # Auto-escalate to human review if confidence is low
        if instance.confidence < 0.6 or instance.outcome == 'requires_review':
            try:
                review = ReviewService.create_review(
                    case_id=str(instance.case.id),
                    auto_assign=True,
                    assignment_strategy='round_robin',
                    review_type='eligibility_check',
                    priority='high' if instance.confidence < 0.4 else 'medium',
                    due_date=None  # Will use default SLA
                )
                if review:
                    logger.info(f"Auto-created review {review.id} for low-confidence eligibility result {instance.id}")
            except Exception as e:
                logger.error(f"Error auto-creating review for eligibility result {instance.id}: {e}")

