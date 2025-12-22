from data_ingestion.models.data_source import DataSource


class DataSourceSelector:
    """Selector for DataSource read operations."""

    @staticmethod
    def get_all():
        """Get all data sources."""
        return DataSource.objects.all()

    @staticmethod
    def get_active():
        """Get all active data sources."""
        return DataSource.objects.filter(is_active=True)

    @staticmethod
    def get_by_jurisdiction(jurisdiction: str):
        """Get data sources by jurisdiction."""
        return DataSource.objects.filter(jurisdiction=jurisdiction, is_active=True)

    @staticmethod
    def get_by_id(data_source_id):
        """Get data source by ID."""
        return DataSource.objects.get(id=data_source_id)

    @staticmethod
    def get_by_base_url(base_url: str):
        """Get data source by base URL."""
        return DataSource.objects.filter(base_url=base_url).first()

