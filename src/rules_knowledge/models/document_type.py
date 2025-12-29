import uuid
from django.db import models


class DocumentType(models.Model):
    """
    Master list of document types (passport, birth certificate, etc.).
    Used in visa document requirements.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    
    code = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="Unique code for the document type (e.g., 'PASSPORT', 'BIRTH_CERT')"
    )
    
    name = models.CharField(
        max_length=255,
        help_text="Human-readable name (e.g., 'Passport', 'Birth Certificate')"
    )
    
    description = models.TextField(
        null=True,
        blank=True,
        help_text="Description of the document type"
    )
    
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Whether this document type is currently active"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'document_types'
        ordering = ['code']
        verbose_name_plural = 'Document Types'

    def __str__(self):
        return f"{self.name} ({self.code})"

