"""
Document Classification Prompts

Contains prompt templates for LLM-based document classification.
"""

from document_handling.helpers.document_type_descriptions import get_document_type_description
from document_handling.helpers.classification_guidelines import (
    get_classification_guidelines,
    get_common_document_indicators,
    get_document_indicators_for_types
)
from rules_knowledge.selectors.document_type_selector import DocumentTypeSelector


def build_document_classification_prompt(
    ocr_text: str,
    file_name: str = None,
    possible_types: list = None
) -> str:
    """
    Build comprehensive prompt for document classification.
    
    Args:
        ocr_text: Extracted text from OCR
        file_name: Original file name
        possible_types: List of possible document type codes
        
    Returns:
        Complete formatted prompt string
    """
    # Get document type descriptions (try database first, then fallback)
    document_type_descriptions = _get_document_type_descriptions_with_fallback(possible_types)
    
    # Get classification guidelines
    guidelines = get_classification_guidelines()
    
    # Get document indicators for available types
    document_indicators = get_document_indicators_for_types(possible_types)
    
    # Build prompt
    prompt = f"""You are an expert document classification system for immigration visa applications. 
Your task is to accurately classify documents based on their content, structure, and key indicators.

## Available Document Types:
{document_type_descriptions}

## Document Information:
- Filename: {file_name or 'unknown'}
- Extracted Text (first 3000 characters):
{ocr_text[:3000]}

## Classification Guidelines:

{guidelines}

4. **Common Document Type Indicators**:

{document_indicators if document_indicators else get_common_document_indicators()}

## Your Task:
Analyze the document and classify it. Respond with ONLY valid JSON in this exact format:
{{
  "document_type": "passport",
  "confidence": 0.95,
  "reasoning": "Document contains passport number, photo page, issuing authority 'HM Passport Office', nationality 'British', and expiry date. Clear passport indicators present."
}}

**Important**: 
- The "document_type" MUST be one of the available types listed above (case-sensitive)
- Confidence must be between 0.0 and 1.0
- Provide detailed reasoning explaining which indicators led to the classification
- Only respond with valid JSON, no markdown, no additional text"""

    return prompt


def _get_document_type_descriptions_with_fallback(possible_types: list) -> str:
    """
    Get document type descriptions, trying database first, then falling back to defaults.
    
    Args:
        possible_types: List of document type codes
        
    Returns:
        Formatted string with document type descriptions
    """
    if not possible_types:
        return "No document types available."
    
    type_list = []
    for doc_type_code in possible_types:
        # Try to get from database first
        try:
            doc_type = DocumentTypeSelector.get_by_code(doc_type_code)
            description = doc_type.description or doc_type.name
            type_list.append(f"- **{doc_type_code}**: {description}")
        except:
            # Fall back to default descriptions
            doc_info = get_document_type_description(doc_type_code)
            description = doc_info['description']
            type_list.append(f"- **{doc_type_code}**: {description}")
    
    return '\n'.join(type_list) if type_list else "No document types available."


def get_system_message() -> str:
    """
    Get system message for LLM classification.
    
    Returns:
        System message string
    """
    return (
        "You are a precise document classification assistant for immigration visa applications. "
        "You analyze documents and classify them into specific types. "
        "Always respond with valid JSON only, no markdown formatting, no additional text."
    )

