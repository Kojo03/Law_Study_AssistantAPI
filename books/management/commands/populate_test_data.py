from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from books.models import Subject, Topic, Quiz, Answer
from cases.models import Case

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate database with test data for Postman testing'

    def handle(self, *args, **options):
        # Create test users
        if not User.objects.filter(username='student1').exists():
            student = User.objects.create_user(
                username='student1',
                email='student@test.com',
                password='testpass123',
                role='student'
            )
            self.stdout.write(f'Created student: {student.username}')

        if not User.objects.filter(username='lecturer1').exists():
            lecturer = User.objects.create_user(
                username='lecturer1',
                email='lecturer@test.com',
                password='testpass123',
                role='lecturer'
            )
            self.stdout.write(f'Created lecturer: {lecturer.username}')

        # Create subjects
        subject1, created = Subject.objects.get_or_create(
            title='Constitutional Law',
            defaults={'description': 'Study of constitutional principles and cases'}
        )
        if created:
            self.stdout.write(f'Created subject: {subject1.title}')

        subject2, created = Subject.objects.get_or_create(
            title='Criminal Law',
            defaults={'description': 'Study of criminal law principles and procedures'}
        )
        if created:
            self.stdout.write(f'Created subject: {subject2.title}')

        # Create topics
        topic1, created = Topic.objects.get_or_create(
            subject=subject1,
            title='Fundamental Rights',
            defaults={'description': 'Basic rights guaranteed by the constitution'}
        )
        if created:
            self.stdout.write(f'Created topic: {topic1.title}')

        topic2, created = Topic.objects.get_or_create(
            subject=subject2,
            title='Criminal Procedure',
            defaults={'description': 'Procedures followed in criminal cases'}
        )
        if created:
            self.stdout.write(f'Created topic: {topic2.title}')

        # Create quizzes
        quiz1, created = Quiz.objects.get_or_create(
            topic=topic1,
            defaults={'question': 'Which amendment guarantees freedom of speech?'}
        )
        if created:
            Answer.objects.create(quiz=quiz1, text='First Amendment', is_correct=True)
            Answer.objects.create(quiz=quiz1, text='Second Amendment', is_correct=False)
            Answer.objects.create(quiz=quiz1, text='Fourth Amendment', is_correct=False)
            self.stdout.write(f'Created quiz: {quiz1.question}')

        # Create cases
        case1, created = Case.objects.get_or_create(
            topic=topic1,
            title='Brown v. Board of Education',
            defaults={
                'summary': 'Landmark case that declared racial segregation in public schools unconstitutional',
                'citation': '347 U.S. 483 (1954)',
                'year': 1954
            }
        )
        if created:
            self.stdout.write(f'Created case: {case1.title}')

        self.stdout.write(self.style.SUCCESS('Test data populated successfully!'))