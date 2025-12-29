from django.apps import AppConfig


class HumanReviewConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "human_reviews"

    def ready(self):
        from .signals import review_signals
