ALLOWED_EXPENSE_METADATA_KEYS = {
    'receipt_url': str,                # Receipt image or file URL
    'tax_deductible': bool,            # Mark if this expense is deductible
    'travel_for': str,                 # Travel purpose (e.g., "Business", "Vacation")
    'ai_category_confidence': float,   # Confidence score from AI categorization
    'reimbursable': bool,              # Whether user can claim reimbursement
    'reimbursed': bool,                # Whether reimbursement has been received
    'notes': str,                      # Extra user notes
    'vendor_name': str,                # Clean vendor name extracted (ex: "Starbucks")
    'payment_method': str,             # Payment method used ("Credit Card", "Cash", etc.)
    'recurring_id': str,               # If part of recurring series (ex: subscription)
    'receipt_date': str,               # Date on receipt (
}
