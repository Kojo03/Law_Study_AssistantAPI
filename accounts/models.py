from django.contrib.auth.models import AbstractUser
from django.db import models
from .validators import validate_phone_number, validate_safe_text

class User(AbstractUser):
    # Roles: member (default), admin
    ROLE_CHOICES = (
        ("member", "Library Member"),
        ("admin", "Administrator"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="member")
    
    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser
    
    @property
    def is_member(self):
        return self.role == 'member'
    phone_number = models.CharField(max_length=15, blank=True, validators=[validate_phone_number])
    address = models.TextField(blank=True, validators=[validate_safe_text])
    membership_date = models.DateField(auto_now_add=True)
    is_active_member = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
