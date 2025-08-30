from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import BookCheckout, Reservation

def notify_book_availability():
    """Notify users when reserved books become available"""
    pass

def check_overdue_books():
    """Check and notify about overdue books"""
    overdue_checkouts = BookCheckout.objects.filter(
        is_returned=False, 
        due_date__lt=timezone.now()
    )
    
    count = 0
    for checkout in overdue_checkouts:
        checkout.calculate_fine()
        count += 1
    
    return count