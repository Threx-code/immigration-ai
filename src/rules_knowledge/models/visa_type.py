import uuid
from django.db import models


class VisaType(models.Model):
    """
    Master list of visa routes (Skilled Worker, Student, Family, etc.).
    Each visa type can have multiple rule versions over time.
    """
    JURISDICTION_CHOICES = [
        ('UK', 'United Kingdom'),
        ('US', 'United States'),
        ('CA', 'Canada'),
        ('AU', 'Australia'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    
    jurisdiction = models.CharField(
        max_length=10,
        choices=JURISDICTION_CHOICES,
        db_index=True,
        help_text="Jurisdiction this visa type belongs to"
    )
    
    code = models.CharField(
        max_length=100,
        db_index=True,
        help_text="Unique code for the visa type (e.g., 'SKILLED_WORKER', 'STUDENT')"
    )
    
    name = models.CharField(
        max_length=255,
        help_text="Human-readable name (e.g., 'Skilled Worker Visa', 'Student Visa')"
    )
    
    description = models.TextField(
        null=True,
        blank=True,
        help_text="Description of the visa type"
    )
    
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Whether this visa type is currently active"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'visa_types'
        ordering = ['jurisdiction', 'code']
        unique_together = [['jurisdiction', 'code']]
        indexes = [
            models.Index(fields=['jurisdiction', 'is_active']),
        ]
        verbose_name_plural = 'Visa Types'

    def __str__(self):
        return f"{self.name} ({self.jurisdiction})"

