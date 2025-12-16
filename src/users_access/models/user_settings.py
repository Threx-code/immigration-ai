from django.db import models
import uuid
from django.conf import settings


class UserSetting(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_settings',
        db_index=True
    )

    # Security and Account Settings
    two_factor_auth = models.BooleanField(default=False)
    totp_secret = models.CharField(max_length=50, null=True, blank=True)
    allow_manual_transactions = models.BooleanField(default=True)

    # Notifications and Alerts Settings
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)

    transaction_alerts = models.BooleanField(default=True)
    low_balance_alerts = models.BooleanField(default=True)
    min_balance_threshold = models.DecimalField(
        max_digits=10, decimal_places=2, default=1000.00,
        help_text="Minimum balance threshold for low balance alerts"
    )
    bill_reminders = models.BooleanField(default=True)
    bill_reminder_days_before_due = models.PositiveIntegerField(default=3)
    upcoming_payment_reminders = models.BooleanField(default=True)
    preferred_reminder_channel = models.CharField(
        max_length=20,
        choices=[("email", "Email"), ("sms", "SMS"), ("push", "Push Notification")],
        default="email",
        db_index=True
    )

    # Budgeting and Financial Goals
    budget_tracking_enabled = models.BooleanField(default=True)
    budget_alert_threshold = models.DecimalField(
        max_digits=10, decimal_places=2, default=1000.00,
        help_text="Threshold for budget alerts"
    )
    savings_goal_tracking = models.BooleanField(default=True)
    monthly_savings_target = models.DecimalField(
        max_digits=10, decimal_places=2, default=500.00,
        help_text="Monthly savings target for financial goals"
    )
    debt_tracking = models.BooleanField(default=True)
    investment_tracking = models.BooleanField(default=True)
    investment_risk_preference = models.CharField(
        max_length=20,
        choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")],
        default="medium",
        help_text="Preferred risk level for investments"
    )

    # Analytics and Reporting
    ai_recommendations = models.BooleanField(default=True)
    spending_report = models.BooleanField(default=True)
    income_report = models.BooleanField(default=True)
    budget_report = models.BooleanField(default=True)
    debt_report = models.BooleanField(default=True)
    investment_report = models.BooleanField(default=True)
    report_frequency = models.CharField(
        max_length=10,
        choices=[("weekly", "Weekly"), ("monthly", "Monthly"), ("quarterly", "Quarterly")],
        default="monthly",
        help_text="Frequency of financial reports"
    )

    # App Preferences
    dark_mode = models.BooleanField(default=False)
    default_dashboards_views = models.JSONField(
        default=dict,
        help_text="Default views for dashboards, e.g., {'requests': 'list', 'bills': 'calendar'}"
    )
    # Tax Reminders and Filing Notifications
    tax_reminders_enabled = models.BooleanField(default=True)
    tax_reminder_frequency = models.CharField(
        max_length=10,
        choices=[("monthly", "Monthly"), ("quarterly", "Quarterly"), ("annually", "Annually")],
        default="annually"
    )
    tax_reminder_days_before_due = models.PositiveIntegerField(default=7)


    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'user_settings'
        ordering = ['-created_at']


    def __str__(self):
        return f"Settings for {self.user.email}"
