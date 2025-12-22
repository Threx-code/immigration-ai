from data_ingestion.models.source_document import SourceDocument


class SourceDocumentSelector:
    """Selector for SourceDocument read operations."""

    @staticmethod
    def get_all():
        """Get all source documents."""
        return SourceDocument.objects.select_related('data_source').all()

    @staticmethod
    def get_by_data_source(data_source):
        """Get source documents by data source."""
        return SourceDocument.objects.select_related('data_source').filter(
            data_source=data_source
        ).order_by('-fetched_at')

    @staticmethod
    def get_by_url(source_url: str):
        """Get source document by URL."""
        return SourceDocument.objects.select_related('data_source').filter(
            source_url=source_url
        ).order_by('-fetched_at').first()

    @staticmethod
    def get_latest_by_data_source(data_source):
        """Get latest source document for a data source."""
        return SourceDocument.objects.select_related('data_source').filter(
            data_source=data_source
        ).order_by('-fetched_at').first()

    @staticmethod
    def get_by_id(document_id):
        """Get source document by ID."""
        return SourceDocument.objects.select_related('data_source').get(id=document_id)

