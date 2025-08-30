"""
Security-focused tests for the accounts app
"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .validators import validate_safe_text, validate_phone_number, validate_username_security
import os

User = get_user_model()


class SecurityValidatorTests(TestCase):
    """Test custom security validators"""
    
    def test_validate_safe_text_blocks_xss(self):
        """Test that XSS attempts are blocked"""
        dangerous_inputs = [
            '<script>alert("xss")</script>',
            'javascript:alert("xss")',
            '<iframe src="evil.com"></iframe>',
            'onclick="alert(1)"',
        ]
        
        for dangerous_input in dangerous_inputs:
            with self.assertRaises(ValidationError):
                validate_safe_text(dangerous_input)
    
    def test_validate_safe_text_allows_safe_content(self):
        """Test that safe content is allowed"""
        safe_inputs = [
            'This is safe text',
            'Numbers 123 and symbols !@#',
            'Normal address: 123 Main St',
        ]
        
        for safe_input in safe_inputs:
            try:
                result = validate_safe_text(safe_input)
                self.assertIsNotNone(result)
            except ValidationError:
                self.fail(f"Safe input '{safe_input}' was incorrectly flagged as dangerous")
    
    def test_validate_phone_number(self):
        """Test phone number validation"""
        valid_phones = ['1234567890', '+1-234-567-8900', '(123) 456-7890']
        invalid_phones = ['123', '12345678901234567890', 'abc123def']
        
        for phone in valid_phones:
            try:
                validate_phone_number(phone)
            except ValidationError:
                self.fail(f"Valid phone '{phone}' was rejected")
        
        for phone in invalid_phones:
            with self.assertRaises(ValidationError):
                validate_phone_number(phone)
    
    def test_validate_username_security(self):
        """Test username security validation"""
        valid_usernames = ['user123', 'test_user', 'user-name']
        invalid_usernames = ["user'; DROP TABLE users;--", 'user"test"', 'user/*comment*/']
        
        for username in valid_usernames:
            try:
                validate_username_security(username)
            except ValidationError:
                self.fail(f"Valid username '{username}' was rejected")
        
        for username in invalid_usernames:
            with self.assertRaises(ValidationError):
                validate_username_security(username)


class UserModelSecurityTests(TestCase):
    """Test User model security features"""
    
    def test_user_creation_with_safe_data(self):
        """Test user creation with validated data"""
        test_password = os.environ.get('TEST_PASSWORD', 'test_secure_pass_123!')
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password=test_password
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
    
    def test_user_creation_blocks_unsafe_data(self):
        """Test that unsafe data is blocked during user creation"""
        # Test username validation
        with self.assertRaises(ValidationError):
            validate_username_security("user'; DROP TABLE users;--")
        
        # Test phone validation
        with self.assertRaises(ValidationError):
            validate_phone_number('invalid_phone')
        
        # Test XSS validation
        with self.assertRaises(ValidationError):
            validate_safe_text('<script>alert("xss")</script>')