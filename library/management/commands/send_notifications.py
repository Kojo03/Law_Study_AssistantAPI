from django.core.management.base import BaseCommand
from library.notifications import check_overdue_books, notify_book_availability

class Command(BaseCommand):
    help = 'Send notifications for overdue books and book availability'

    def handle(self, *args, **options):
        overdue_count = check_overdue_books()
        available_count = notify_book_availability()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Sent {overdue_count} overdue notifications and {available_count} availability notifications'
            )
        )