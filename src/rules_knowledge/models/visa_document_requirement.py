import uuid
from django.db import models
from .visa_rule_version import VisaRuleVersion
from .document_type import DocumentType


class VisaDocumentRequirement(models.Model):
    """
    Document checklist per visa route and rule version.
    Links visa types to required document types.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    
    rule_version = models.ForeignKey(
        VisaRuleVersion,
        on_delete=models.CASCADE,
        related_name='document_requirements',
        db_index=True,
        help_text="The rule version this document requirement belongs to"
    )
    
    document_type = models.ForeignKey(
        DocumentType,
        on_delete=models.CASCADE,
        related_name='visa_requirements',
        db_index=True,
        help_text="The document type required"
    )
    
    mandatory = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Whether this document is mandatory"
    )
    
    conditional_logic = models.JSONField(
        null=True,
        blank=True,
        help_text="Optional JSON Logic for conditional requirements (e.g., dependants)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'visa_document_requirements'
        unique_together = [['rule_version', 'document_type']]
        indexes = [
            models.Index(fields=['rule_version', 'mandatory']),
        ]
        verbose_name_plural = 'Visa Document Requirements'

    def __str__(self):
        return f"{self.document_type.name} - {self.rule_version.visa_type.name}"

