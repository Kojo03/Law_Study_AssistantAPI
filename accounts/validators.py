from django.core.exceptions import ValidationError
from django.utils.html import escape
import re

def validate_phone_number(value):
    """Validate phone number format"""
    if value and not re.match(r'^[\d\s\-\+\(\)]{10,15}$', value):
        raise ValidationError('Enter a valid phone number.')

def validate_safe_text(value):
    """Validate and sanitize text input"""
    if value:
        # Basic HTML tag removal and escaping
        cleaned = escape(value)
        if len(cleaned) > 1000:  # Reasonable limit
            raise ValidationError('Text is too long.')
        return cleaned
    return value