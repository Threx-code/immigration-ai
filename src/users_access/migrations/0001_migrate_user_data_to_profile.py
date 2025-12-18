"""
Data migration to split User model and move PII to UserProfile.

This migration:
1. Creates UserProfile records for existing users
2. Moves first_name, last_name, avatar from User to UserProfile
3. Keeps User model with auth/authorization fields only

Run this AFTER creating the UserProfile model migration.
"""

from django.db import migrations


def migrate_user_data_to_profile(apps, schema_editor):
    """
    Migrate existing user PII data to UserProfile.
    """
    User = apps.get_model('users_access', 'User')
    UserProfile = apps.get_model('users_access', 'UserProfile')
    
    # Check if UserProfile table exists (it should after model migration)
    db_alias = schema_editor.connection.alias
    
    users_without_profile = User.objects.using(db_alias).filter(
        profile__isnull=True
    )
    
    migrated_count = 0
    for user in users_without_profile:
        # Get old fields (these will be removed in schema migration)
        first_name = getattr(user, 'first_name', None)
        last_name = getattr(user, 'last_name', None)
        avatar = getattr(user, 'avatar', None)
        
        # Create profile with migrated data
        UserProfile.objects.using(db_alias).create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            avatar=avatar
        )
        migrated_count += 1
    
    print(f"Migrated {migrated_count} user profiles")


def reverse_migration(apps, schema_editor):
    """
    Reverse migration - move data back to User model.
    Note: This assumes User model still has first_name, last_name, avatar fields.
    If those fields were removed, this will fail.
    """
    User = apps.get_model('users_access', 'User')
    UserProfile = apps.get_model('users_access', 'UserProfile')
    
    db_alias = schema_editor.connection.alias
    
    for profile in UserProfile.objects.using(db_alias).all():
        user = profile.user
        # Only update if User model still has these fields
        if hasattr(user, 'first_name'):
            user.first_name = profile.first_name
        if hasattr(user, 'last_name'):
            user.last_name = profile.last_name
        if hasattr(user, 'avatar'):
            user.avatar = profile.avatar
        user.save(using=db_alias)


class Migration(migrations.Migration):
    """
    This migration should run AFTER the schema migration that:
    1. Creates UserProfile model
    2. Removes first_name, last_name, avatar from User model
    """
    
    dependencies = [
        ('users_access', '0000_initial'),  # Update with your actual initial migration
    ]

    operations = [
        migrations.RunPython(
            migrate_user_data_to_profile,
            reverse_migration,
        ),
    ]

