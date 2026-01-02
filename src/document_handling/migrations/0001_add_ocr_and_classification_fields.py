# Generated migration to add OCR and classification fields to CaseDocument

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document_handling', '__first__'),
    ]

    operations = [
        migrations.AddField(
            model_name='casedocument',
            name='ocr_text',
            field=models.TextField(blank=True, help_text='Extracted text from OCR processing', null=True),
        ),
        migrations.AddField(
            model_name='casedocument',
            name='classification_confidence',
            field=models.FloatField(blank=True, help_text='Confidence score for document type classification (0.0 to 1.0)', null=True),
        ),
    ]

