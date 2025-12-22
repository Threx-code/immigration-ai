from data_ingestion.models.document_diff import DocumentDiff

class DocumentDiffSelector:
    """Selector for DocumentDiff read operations."""

    @staticmethod
    def get_all():
        """Get all document diffs."""
        return DocumentDiff.objects.select_related(
            'old_version', 'new_version',
            'old_version__source_document',
            'new_version__source_document'
        ).all()

    @staticmethod
    def get_by_versions(old_version, new_version):
        """Get diff between two versions."""
        return DocumentDiff.objects.select_related(
            'old_version', 'new_version',
            'old_version__source_document',
            'new_version__source_document'
        ).filter(old_version=old_version, new_version=new_version).first()

    @staticmethod
    def get_by_change_type(change_type: str):
        """Get diffs by change type."""
        return DocumentDiff.objects.select_related(
            'old_version', 'new_version',
            'old_version__source_document',
            'new_version__source_document'
        ).filter(change_type=change_type).order_by('-created_at')

    @staticmethod
    def get_by_id(diff_id):
        """Get document diff by ID."""
        return DocumentDiff.objects.select_related(
            'old_version', 'new_version',
            'old_version__source_document',
            'new_version__source_document'
        ).get(id=diff_id)

