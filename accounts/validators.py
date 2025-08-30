import re
from django.core.exceptions import ValidationError
from django.utils.html import escape

def validate_phone_number(value):
    """Validate phone number format"""
    if value and not re.match(r'^\+?[\d\s\-\(\)]{10,15}$', value):
        raise ValidationError('Invalid phone number format')

def validate_safe_text(value):
    """Validate and sanitize text input"""
    if value:
        # Basic XSS prevention
        dangerous_chars = ['<', '>', '"', "'", '&']
        for char in dangerous_chars:
            if char in value:
                raise ValidationError('Invalid characters in text')
    return escape(str(value)) if value else value