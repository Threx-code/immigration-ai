import json
import logging
from typing import Dict, Optional, List
from helpers.request.client import Client
from .base_ingestion import BaseIngestionSystem

logger = logging.getLogger('django')


class UKIngestionSystem(BaseIngestionSystem):
    """
    UK-specific ingestion system for gov.uk API.
    Handles the UK government's content API structure (JSON-based).
    Reference: https://www.gov.uk/api/content/entering-staying-uk
    
    Uses helpers.request.client.Client for all HTTP requests.
    """
    
    def __init__(self, data_source):
        super().__init__(data_source)
        self.api_base = "https://www.gov.uk"
        self.client = Client(base_url=self.api_base)
        self.headers = {
            'User-Agent': 'ImmigrationIntelligenceBot/1.0',
            'Accept': 'application/json'
        }
    
    def fetch_content(self, url: str) -> Optional[Dict]:
        """
        Fetch content from gov.uk API (JSON API).
        Uses helpers.request.client.Client.get_with_details() for detailed response information.
        
        Args:
            url: API URL to fetch from (e.g., https://www.gov.uk/api/content/entering-staying-uk)
            
        Returns:
            Dict with 'content', 'content_type', 'status_code', 'error'
        """
        # Extract endpoint from full URL
        endpoint = url.replace(self.api_base, '')
        
        # Use Client.get_with_details() for detailed response information
        return self.client.get_with_details(
            endpoint=endpoint,
            headers=self.headers,
            timeout=30
        )
    
    def extract_text(self, raw_content: str, content_type: str) -> str:
        """
        Extract clean text from JSON API response.
        
        Args:
            raw_content: Raw JSON content as string
            content_type: Content type (should be application/json)
            
        Returns:
            Extracted text content
        """
        try:
            data = json.loads(raw_content)
            return self._extract_text_from_json(data)
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse JSON, returning raw content")
            return raw_content
    
    def _extract_text_from_json(self, data: Dict, depth: int = 0) -> str:
        """
        Recursively extract text from gov.uk API JSON structure.
        Extracts title, description, details.internal_name, and other text fields.
        Based on actual API response structure from uk_ingestion.json.
        """
        if depth > 10:  # Prevent infinite recursion
            return ""
        
        text_parts = []
        
        # Extract top-level text fields (handle null values)
        if data.get('title'):
            text_parts.append(str(data['title']))
        
        if data.get('description'):
            text_parts.append(str(data['description']))
        
        # Extract from details object (common in gov.uk API)
        if 'details' in data and isinstance(data['details'], dict):
            if data['details'].get('internal_name'):
                text_parts.append(str(data['details']['internal_name']))
            # Skip notes_for_editors and visible_to_departmental_editors as they're not content
        
        # Extract schema_name and document_type for context
        if data.get('schema_name'):
            text_parts.append(str(data['schema_name']))
        
        # Note: We don't recursively process child_taxons here to avoid duplicating content
        # Child taxons will be processed separately when their URLs are fetched
        
        return ' '.join(filter(None, text_parts))  # Filter out empty strings
    
    def parse_api_response(self, response: Dict) -> List[Dict]:
        """
        Parse gov.uk API response to extract child taxon URLs.
        Based on actual API response structure from uk_ingestion.json.
        
        Args:
            response: API response as dictionary
            
        Returns:
            List of documents/URLs to process (only child taxons, not parent taxons)
        """
        documents = []
        
        # Process child taxons from links.child_taxons
        # Note: We don't add the current document here as it's already being processed
        # We only extract child URLs to fetch recursively
        if 'links' in response and isinstance(response['links'], dict):
            if 'child_taxons' in response['links']:
                for child in response['links']['child_taxons']:
                    # Only process if it has an api_url and is not withdrawn
                    if child.get('api_url') and not child.get('withdrawn', False):
                        documents.append({
                            'url': child['api_url'],
                            'title': child.get('title', ''),
                            'base_path': child.get('base_path', ''),
                        })
        
        return documents
    
    def get_document_urls(self) -> List[str]:
        """
        Get list of document URLs to fetch from the UK gov.uk API.
        Recursively fetches ALL child taxons from the base URL.
        Stores all endpoint data as per implementation.md requirements.
        
        Returns:
            List of URLs to fetch (all endpoints including nested children)
        """
        import time
        
        urls = []
        base_url = self.data_source.base_url
        visited_urls = set()
        
        def _fetch_recursive(url: str, max_depth: int = 10):
            """
            Recursively fetch child taxons.
            Increased max_depth to ensure all nested children are fetched.
            """
            if max_depth <= 0 or url in visited_urls:
                return
            
            visited_urls.add(url)
            urls.append(url)
            
            # Rate limiting: 1 request per 2 seconds per domain (as per implementation.md)
            if len(urls) > 1:
                time.sleep(2)
            
            # Fetch the URL
            response_data = self.fetch_content(url)
            if response_data and response_data.get('content'):
                try:
                    api_response = json.loads(response_data['content'])
                    child_docs = self.parse_api_response(api_response)
                    
                    # Recursively process ALL child taxons
                    for doc in child_docs:
                        if doc['url'] not in visited_urls:
                            _fetch_recursive(doc['url'], max_depth - 1)
                            
                except (json.JSONDecodeError, KeyError) as e:
                    logger.warning(f"Error parsing API response for {url}: {e}")
            elif response_data and response_data.get('error'):
                logger.error(f"Error fetching {url}: {response_data.get('error')}")
        
        # Start recursive fetching from base URL
        _fetch_recursive(base_url)
        
        logger.info(f"Found {len(urls)} URLs to process from {base_url}")
        return urls

