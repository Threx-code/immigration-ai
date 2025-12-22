from abc import ABC, abstractmethod
from typing import Dict, Optional, List
import logging

logger = logging.getLogger('django')


class BaseIngestionSystem(ABC):
    """
    Abstract base class for jurisdiction-specific ingestion systems.
    Each jurisdiction (UK, US, Canada, etc.) implements this interface.
    """
    
    def __init__(self, data_source):
        """
        Initialize the ingestion system with a data source.
        
        Args:
            data_source: DataSource model instance
        """
        self.data_source = data_source
        self.jurisdiction = data_source.jurisdiction
    
    @abstractmethod
    def fetch_content(self, url: str) -> Optional[Dict]:
        """
        Fetch content from the source URL.
        
        Args:
            url: URL to fetch from
            
        Returns:
            Dict with keys: 'content', 'content_type', 'status_code', 'error' (if any)
            Returns None if fetch failed
        """
        pass
    
    @abstractmethod
    def extract_text(self, raw_content: str, content_type: str) -> str:
        """
        Extract clean text from raw content.
        
        Args:
            raw_content: Raw content as fetched
            content_type: Content type (text/html, application/json, etc.)
            
        Returns:
            Extracted text content
        """
        pass
    
    @abstractmethod
    def parse_api_response(self, response: Dict) -> List[Dict]:
        """
        Parse API response to extract document URLs or content.
        
        Args:
            response: API response as dictionary
            
        Returns:
            List of documents/URLs to process
        """
        pass
    
    @abstractmethod
    def get_document_urls(self) -> List[str]:
        """
        Get list of document URLs to fetch from the data source.
        
        Returns:
            List of URLs to fetch
        """
        pass
    
    def get_base_url(self) -> str:
        """Get the base URL for this data source."""
        return self.data_source.base_url

