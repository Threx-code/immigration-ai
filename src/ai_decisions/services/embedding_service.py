import logging
from typing import List, Dict, Optional
from django.conf import settings

logger = logging.getLogger('django')


class EmbeddingService:
    """
    Service for generating text embeddings using OpenAI API.
    Handles chunking, embedding generation, and error handling.
    """

    # OpenAI text-embedding-ada-002 dimensions
    EMBEDDING_DIMENSIONS = 1536
    # Maximum tokens per chunk (roughly 8000 characters)
    MAX_CHUNK_SIZE = 8000
    # Overlap between chunks for context preservation
    CHUNK_OVERLAP = 200

    @staticmethod
    def chunk_document(text: str, chunk_size: int = None, overlap: int = None) -> List[Dict]:
        """
        Split document text into chunks for embedding.
        
        Args:
            text: Full document text
            chunk_size: Maximum characters per chunk (default: MAX_CHUNK_SIZE)
            overlap: Characters to overlap between chunks (default: CHUNK_OVERLAP)
            
        Returns:
            List of dicts with 'text' and 'metadata' keys
        """
        if not text or len(text.strip()) == 0:
            return []
        
        chunk_size = chunk_size or EmbeddingService.MAX_CHUNK_SIZE
        overlap = overlap or EmbeddingService.CHUNK_OVERLAP
        
        chunks = []
        start = 0
        chunk_index = 0
        
        while start < len(text):
            # Calculate chunk end
            end = min(start + chunk_size, len(text))
            
            # Try to break at sentence boundary (prefer . or \n)
            if end < len(text):
                # Look for sentence boundary within last 200 chars
                boundary_search_start = max(start, end - 200)
                for i in range(end - 1, boundary_search_start - 1, -1):
                    if text[i] in ['.', '\n', '!', '?']:
                        end = i + 1
                        break
            
            chunk_text = text[start:end].strip()
            
            if chunk_text:
                chunks.append({
                    'text': chunk_text,
                    'metadata': {
                        'chunk_index': chunk_index,
                        'start_char': start,
                        'end_char': end,
                        'length': len(chunk_text)
                    }
                })
                chunk_index += 1
            
            # Move start position with overlap
            start = max(end - overlap, start + 1)
            if start >= len(text):
                break
        
        logger.info(f"Chunked document into {len(chunks)} chunks")
        return chunks

    @staticmethod
    def generate_embeddings(texts: List[str], model: str = "text-embedding-ada-002") -> List[List[float]]:
        """
        Generate embeddings for a list of texts using OpenAI API.
        
        Args:
            texts: List of text strings to embed
            model: OpenAI embedding model (default: text-embedding-ada-002)
            
        Returns:
            List of embedding vectors (each is a list of 1536 floats)
            
        Raises:
            Exception: If OpenAI API call fails
        """
        if not texts:
            return []
        
        try:
            # Import OpenAI client (will be available when openai package is installed)
            try:
                from openai import OpenAI
            except ImportError:
                logger.error("OpenAI package not installed. Install with: pip install openai")
                raise ImportError("OpenAI package required for embedding generation")
            
            # Get API key from settings
            api_key = getattr(settings, 'OPENAI_API_KEY', None)
            if not api_key:
                logger.error("OPENAI_API_KEY not set in settings")
                raise ValueError("OPENAI_API_KEY must be set in settings")
            
            client = OpenAI(api_key=api_key)
            
            # Generate embeddings
            response = client.embeddings.create(
                model=model,
                input=texts
            )
            
            embeddings = [item.embedding for item in response.data]
            
            logger.info(f"Generated {len(embeddings)} embeddings using {model}")
            return embeddings
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise

    @staticmethod
    def generate_embedding(text: str, model: str = "text-embedding-ada-002") -> List[float]:
        """
        Generate a single embedding for text.
        
        Args:
            text: Text to embed
            model: OpenAI embedding model
            
        Returns:
            Embedding vector (list of 1536 floats)
        """
        embeddings = EmbeddingService.generate_embeddings([text], model=model)
        return embeddings[0] if embeddings else []

    @staticmethod
    def validate_embedding(embedding: List[float]) -> bool:
        """
        Validate that embedding has correct dimensions.
        
        Args:
            embedding: Embedding vector to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not embedding:
            return False
        
        if len(embedding) != EmbeddingService.EMBEDDING_DIMENSIONS:
            logger.warning(
                f"Embedding has {len(embedding)} dimensions, "
                f"expected {EmbeddingService.EMBEDDING_DIMENSIONS}"
            )
            return False
        
        return True

