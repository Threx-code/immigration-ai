import uuid
from django.db import models
from .case import Case


class CaseFact(models.Model):
    """
    Flexible key-value store for case data (salary, age, nationality, etc.).
    Append-only facts for auditability.
    """
    SOURCE_CHOICES = [
        ('user', 'User Provided'),
        ('ai', 'AI Derived'),
        ('reviewer', 'Reviewer Corrected'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='facts',
        db_index=True,
        help_text="The case this fact belongs to"
    )
    
    fact_key = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Key for the fact (e.g., 'salary', 'age', 'nationality')"
    )
    
    fact_value = models.JSONField(
        help_text="Value of the fact (can be string, number, boolean, etc.)"
    )
    
    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        default='user',
        db_index=True,
        help_text="Source of the fact"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'case_facts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['case', 'fact_key']),
            models.Index(fields=['fact_key', '-created_at']),
        ]
        verbose_name_plural = 'Case Facts'

    def __str__(self):
        return f"{self.case.id} - {self.fact_key}: {self.fact_value}"

