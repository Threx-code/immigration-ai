import uuid
from django.db import models
from django.conf import settings
from .country import Country
from .state_province import StateProvince


class UserProfile(models.Model):
    """
    User Profile model - GDPR-separated PII and immigration-specific data.
    This separation allows for easier GDPR compliance (right-to-erasure).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        db_index=True
    )
    
    # Personal Information (PII)
    first_name = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    last_name = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    
    # Immigration-specific fields
    nationality = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='nationals',
        db_index=True,
        help_text="User's nationality/country of citizenship"
    )
    
    # State/Province of nationality (optional, for countries with states)
    # e.g., US citizen from California, Indian from Maharashtra
    state_province = models.ForeignKey(
        StateProvince,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='residents',
        db_index=True,
        help_text="State/Province of nationality (if applicable)"
    )
    
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        db_index=True,
        help_text="Date of birth for age-based eligibility checks"
    )
    
    # GDPR Compliance
    consent_given = models.BooleanField(
        default=False,
        db_index=True,
        help_text="User has given consent for data processing"
    )
    consent_timestamp = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When consent was given"
    )
    
    # Optional fields
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_profiles'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['nationality']),
            models.Index(fields=['state_province']),
            models.Index(fields=['date_of_birth']),
        ]
    
    def __str__(self):
        name = f"{self.first_name} {self.last_name}".strip() if self.first_name or self.last_name else "Unnamed"
        return f"Profile for {name} ({self.user.email})"

