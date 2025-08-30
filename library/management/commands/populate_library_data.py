from django.core.management.base import BaseCommand
from library.models import Book, Category
from datetime import date

class Command(BaseCommand):
    help = 'Populate library with sample law books and categories'

    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            {'name': 'Constitutional Law', 'description': 'Books on constitutional principles and cases'},
            {'name': 'Criminal Law', 'description': 'Criminal law cases and procedures'},
            {'name': 'Contract Law', 'description': 'Contract formation, interpretation, and enforcement'},
            {'name': 'Tort Law', 'description': 'Civil wrongs and liability'},
            {'name': 'Administrative Law', 'description': 'Government agency law and procedures'},
            {'name': 'International Law', 'description': 'International legal principles and treaties'},
            {'name': 'Corporate Law', 'description': 'Business and corporate legal matters'},
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Get categories for books
        constitutional = Category.objects.get(name='Constitutional Law')
        criminal = Category.objects.get(name='Criminal Law')
        contract = Category.objects.get(name='Contract Law')
        tort = Category.objects.get(name='Tort Law')
        administrative = Category.objects.get(name='Administrative Law')
        international = Category.objects.get(name='International Law')
        corporate = Category.objects.get(name='Corporate Law')

        # Create sample books
        books_data = [
            {'title': 'Constitutional Law Principles', 'author': 'John Smith', 'isbn': '9781234567890', 
             'published_date': date(2020, 1, 15), 'publisher': 'Legal Press', 'category': constitutional,
             'total_copies': 3, 'description': 'Comprehensive guide to constitutional law principles',
             'location': 'A1-001'},
            {'title': 'Criminal Law Cases', 'author': 'Jane Doe', 'isbn': '9781234567891', 
             'published_date': date(2019, 6, 10), 'publisher': 'Law Books Inc', 'category': criminal,
             'total_copies': 2, 'description': 'Collection of landmark criminal law cases',
             'location': 'B2-015'},
            {'title': 'Contract Law Fundamentals', 'author': 'Robert Johnson', 'isbn': '9781234567892', 
             'published_date': date(2021, 3, 22), 'publisher': 'Academic Law', 'category': contract,
             'total_copies': 4, 'description': 'Essential principles of contract law',
             'location': 'C3-022'},
            {'title': 'Tort Law Analysis', 'author': 'Sarah Wilson', 'isbn': '9781234567893', 
             'published_date': date(2018, 11, 5), 'publisher': 'Legal Studies', 'category': tort,
             'total_copies': 1, 'description': 'In-depth analysis of tort law principles',
             'location': 'D4-008'},
            {'title': 'Administrative Law Guide', 'author': 'Michael Brown', 'isbn': '9781234567894', 
             'published_date': date(2022, 8, 18), 'publisher': 'Government Press', 'category': administrative,
             'total_copies': 5, 'description': 'Complete guide to administrative law procedures',
             'location': 'E5-031'},
            {'title': 'International Law Treaties', 'author': 'Elena Rodriguez', 'isbn': '9781234567895', 
             'published_date': date(2021, 12, 3), 'publisher': 'Global Law', 'category': international,
             'total_copies': 2, 'description': 'Analysis of major international treaties',
             'location': 'F6-012'},
            {'title': 'Corporate Law Handbook', 'author': 'David Chen', 'isbn': '9781234567896', 
             'published_date': date(2023, 2, 14), 'publisher': 'Business Law', 'category': corporate,
             'total_copies': 3, 'description': 'Practical guide to corporate legal matters',
             'location': 'G7-025'},
        ]

        for book_data in books_data:
            book, created = Book.objects.get_or_create(
                isbn=book_data['isbn'],
                defaults=book_data
            )
            if created:
                self.stdout.write(f'Created book: {book.title}')

        self.stdout.write(self.style.SUCCESS('Successfully populated library with law books and categories'))