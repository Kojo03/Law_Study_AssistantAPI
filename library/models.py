from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone

from datetime import timedelta

User = settings.AUTH_USER_MODEL

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    publisher = models.CharField(max_length=255, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    total_copies = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    available_copies = models.PositiveIntegerField(validators=[MinValueValidator(0)], default=0)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True, help_text="Shelf location")
    added_date = models.DateTimeField(default=timezone.now)
    
    def save(self, *args, **kwargs):
        if not self.pk:  # New book
            self.available_copies = self.total_copies
        super().save(*args, **kwargs)
    
    @property
    def is_available(self):
        return self.available_copies > 0
    
    def __str__(self):
        return f"{self.title} by {self.author}"

class BookCheckout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='checkouts')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='checkouts')
    checkout_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'book'],
                condition=models.Q(is_returned=False),
                name='unique_active_checkout'
            )
        ]
    
    def save(self, *args, **kwargs):
        if not self.pk:  # New checkout
            self.due_date = timezone.now() + timedelta(days=14)  # 2 weeks loan period
        # Auto-calculate fine for overdue books
        if self.is_overdue and not self.is_returned:
            self.fine_amount = self.days_overdue * 1.00
        super().save(*args, **kwargs)
    
    @property
    def is_overdue(self):
        return not self.is_returned and timezone.now() > self.due_date
    
    @property
    def days_overdue(self):
        if self.is_overdue:
            return (timezone.now() - self.due_date).days
        return 0
    
    def calculate_fine(self):
        """Calculate fine for overdue books ($1 per day)"""
        if self.is_overdue:
            self.fine_amount = self.days_overdue * 1.00
            self.save()
        return self.fine_amount
    
    def __str__(self):
        from django.utils.html import escape
        return escape(f"{self.user.username} - {self.book.title}")

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reservations')
    reservation_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    notified = models.BooleanField(default=False)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'book'],
                condition=models.Q(is_active=True),
                name='unique_active_reservation'
            )
        ]
    
    def __str__(self):
        return f"{self.user.username} reserved {self.book.title}"

# Transaction model alias for requirement compliance
class Transaction(models.Model):
    """Transaction model to track all book-related activities"""
    TRANSACTION_TYPES = [
        ('checkout', 'Checkout'),
        ('return', 'Return'),
        ('reservation', 'Reservation'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    transaction_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-transaction_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.book.title}"