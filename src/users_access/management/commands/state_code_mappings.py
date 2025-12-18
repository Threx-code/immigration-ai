"""
State/Province code mappings for major immigration jurisdictions.

This file contains mappings from state/province names to their official codes
for countries that are important immigration jurisdictions.
"""

STATE_CODE_MAPPINGS = {
    'CA': {
        'Alberta': 'AB',
        'British Columbia': 'BC',
        'Manitoba': 'MB',
        'New Brunswick': 'NB',
        'Newfoundland and Labrador': 'NL',
        'Northwest Territories': 'NT',
        'Nova Scotia': 'NS',
        'Nunavut': 'NU',
        'Ontario': 'ON',
        'Prince Edward Island': 'PE',
        'Quebec': 'QC',
        'Saskatchewan': 'SK',
        'Yukon': 'YT',
    },
    'AU': {
        'New South Wales': 'NSW',
        'Victoria': 'VIC',
        'Queensland': 'QLD',
        'Western Australia': 'WA',
        'South Australia': 'SA',
        'Tasmania': 'TAS',
        'Australian Capital Territory': 'ACT',
        'Northern Territory': 'NT',
    },
    'US': {
        'Alabama': 'AL',
        'Alaska': 'AK',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY',
        'District of Columbia': 'DC',
    },
}


def get_state_code_from_name(country_code: str, state_name: str) -> str:
    """
    Get state/province code from state name.
    
    Args:
        country_code: ISO 3166-1 alpha-2 country code (e.g., 'CA', 'AU', 'US')
        state_name: Full name of the state/province
        
    Returns:
        Official state/province code, or generated code if no mapping exists
    """
    # Check if we have a mapping for this country and state
    if country_code in STATE_CODE_MAPPINGS:
        state_mappings = STATE_CODE_MAPPINGS[country_code]
        if state_name in state_mappings:
            return state_mappings[state_name]
    
    # Fallback: generate code from name
    words = state_name.split()
    if len(words) == 1:
        # Single word: take first 2-3 letters
        return state_name[:3].upper()
    elif len(words) == 2:
        # Two words: take first letter of each
        return (words[0][0] + words[1][0]).upper()
    else:
        # Multiple words: take first letter of first 2-3 words
        return ''.join([w[0].upper() for w in words[:3]])[:10]

