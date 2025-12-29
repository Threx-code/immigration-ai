import uuid
from django.db import models
from django.utils import timezone
from .visa_type import VisaType


class VisaRuleVersion(models.Model):
    """
    Temporal versioning of immigration rules.
    Each version has an effective date range and links to the source document version.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    
    visa_type = models.ForeignKey(
        VisaType,
        on_delete=models.CASCADE,
        related_name='rule_versions',
        db_index=True,
        help_text="The visa type this rule version applies to"
    )
    
    effective_from = models.DateTimeField(
        db_index=True,
        help_text="When this rule version becomes effective"
    )
    
    effective_to = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
        help_text="When this rule version expires (NULL means current)"
    )
    
    source_document_version = models.ForeignKey(
        'data_ingestion.DocumentVersion',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='rule_versions',
        db_index=True,
        help_text="The document version this rule was extracted from"
    )
    
    is_published = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Whether this rule version is published and available for use"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'visa_rule_versions'
        ordering = ['-effective_from']
        indexes = [
            models.Index(fields=['visa_type', 'effective_from', 'effective_to']),
            models.Index(fields=['is_published', 'effective_from']),
        ]
        verbose_name_plural = 'Visa Rule Versions'

    def __str__(self):
        return f"{self.visa_type.name} - Version {self.effective_from.date()}"

    def is_current(self):
        """Check if this rule version is currently effective."""
        now = timezone.now()
        if self.effective_to:
            return self.effective_from <= now <= self.effective_to
        return self.effective_from <= now

