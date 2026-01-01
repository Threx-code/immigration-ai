"""
Management command to create or update the UK data source for ingestion.

Usage:
    python manage.py setup_uk_data_source
    python manage.py setup_uk_data_source --update
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from data_ingestion.services.data_source_service import DataSourceService
from data_ingestion.selectors.data_source_selector import DataSourceSelector
import logging

logger = logging.getLogger('django')


class Command(BaseCommand):
    help = 'Create or update the UK data source for ingestion'

    def add_arguments(self, parser):
        parser.add_argument(
            '--update',
            action='store_true',
            help='Update existing data source if it exists',
        )
        parser.add_argument(
            '--base-url',
            type=str,
            help='Custom base URL for the UK Gov API (overrides settings)',
        )
        parser.add_argument(
            '--crawl-frequency',
            type=str,
            default='weekly',
            choices=['hourly', 'daily', 'weekly', 'monthly'],
            help='Crawl frequency (default: weekly)',
        )

    def handle(self, *args, **options):
        # Get base URL from options, settings, or default
        base_url = options.get('base_url')
        if not base_url:
            base_url = getattr(
                settings,
                'UK_GOV_API_BASE_URL',
                'https://www.gov.uk/api/content/entering-staying-uk'
            )
        
        crawl_frequency = options.get('crawl_frequency', 'weekly')
        
        # Check if UK data source already exists
        try:
            existing_sources = DataSourceSelector.get_by_jurisdiction('UK')
            uk_source = existing_sources.filter(
                base_url=base_url
            ).first()
            
            if uk_source:
                if options.get('update'):
                    # Update existing source
                    self.stdout.write(
                        self.style.WARNING(
                            f'Updating existing UK data source: {uk_source.id}'
                        )
                    )
                    updated = DataSourceService.update_data_source(
                        uk_source,
                        name="UK Gov Immigration API",
                        base_url=base_url,
                        crawl_frequency=crawl_frequency,
                        is_active=True
                    )
                    if updated:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Successfully updated UK data source: {updated.id}'
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.ERROR('Failed to update data source')
                        )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'UK data source already exists: {uk_source.id}\n'
                            f'  Name: {uk_source.name}\n'
                            f'  Base URL: {uk_source.base_url}\n'
                            f'  Active: {uk_source.is_active}\n'
                            f'  Crawl Frequency: {uk_source.crawl_frequency}\n'
                            f'\nUse --update flag to update it.'
                        )
                    )
                    return
            else:
                # Create new data source
                self.stdout.write('Creating new UK data source...')
                data_source = DataSourceService.create_data_source(
                    name="UK Gov Immigration API",
                    base_url=base_url,
                    jurisdiction="UK",
                    crawl_frequency=crawl_frequency,
                    is_active=True
                )
                
                if data_source:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Successfully created UK data source:\n'
                            f'  ID: {data_source.id}\n'
                            f'  Name: {data_source.name}\n'
                            f'  Base URL: {data_source.base_url}\n'
                            f'  Jurisdiction: {data_source.jurisdiction}\n'
                            f'  Crawl Frequency: {data_source.crawl_frequency}\n'
                            f'  Active: {data_source.is_active}\n'
                            f'\nYou can now trigger ingestion:\n'
                            f'  - Via API: POST /api/v1/data-ingestion/data-sources/{data_source.id}/ingest/\n'
                            f'  - Via Celery: Will run automatically weekly (Sunday 2 AM UTC)\n'
                            f'  - Via Django shell:\n'
                            f'    from data_ingestion.services.data_source_service import DataSourceService\n'
                            f'    DataSourceService.trigger_ingestion("{data_source.id}")'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR('Failed to create data source')
                    )
                    
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error: {e}')
            )
            logger.error(f"Error in setup_uk_data_source command: {e}", exc_info=True)

