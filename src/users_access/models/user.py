import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.db import models


class User(AbstractBaseUser, PermissionsMixin):
    """
    User model - Authentication and authorization only.
    PII data is stored in UserProfile model for GDPR compliance.
    """
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
        ('reviewer', 'Reviewer'),  # Added reviewer role from spec
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    
    # Authentication
    email = models.EmailField(max_length=255, unique=True, null=False, db_index=True)
    password = models.CharField(max_length=255, null=False)
    is_verified = models.BooleanField(default=False, db_index=True)
    is_active = models.BooleanField(default=True)

    # User Role & Permissions
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user', db_index=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    login_count = models.PositiveIntegerField(default=0, db_index=True)
    
    # Reviewer assignment tracking (from implementation spec)
    last_assigned_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
        help_text="Last time reviewer was assigned a review (for round-robin assignment)"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    # User Groups & Permissions
    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name='custom_user_group',
        related_query_name='user',
        db_index=True
    )

    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='custom_user_permissions',
        related_query_name='user',
        db_index=True
    )

    USERNAME_FIELD = 'email'

    def __str__(self):
        return f"User ({self.email})"