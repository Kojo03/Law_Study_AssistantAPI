from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from accounts.models import User
from .models import Subject, Topic, Note, Quiz, Answer

class BookModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.subject = Subject.objects.create(
            title='Constitutional Law',
            description='Study of constitutional principles'
        )
        self.topic = Topic.objects.create(
            subject=self.subject,
            title='Fundamental Rights',
            description='Basic rights guaranteed by constitution'
        )
        
    def test_subject_creation(self):
        self.assertEqual(self.subject.title, 'Constitutional Law')
        self.assertEqual(str(self.subject), 'Constitutional Law')
        
    def test_topic_creation(self):
        self.assertEqual(self.topic.title, 'Fundamental Rights')
        self.assertEqual(self.topic.subject, self.subject)
        
    def test_note_creation(self):
        note = Note.objects.create(
            user=self.user,
            topic=self.topic,
            content='Important notes on fundamental rights'
        )
        self.assertEqual(note.user, self.user)
        self.assertEqual(note.topic, self.topic)

class BooksAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        
        self.subject = Subject.objects.create(
            title='Constitutional Law',
            description='Study of constitutional principles'
        )
        self.topic = Topic.objects.create(
            subject=self.subject,
            title='Fundamental Rights'
        )
        
    def test_subject_list(self):
        url = '/books/subjects/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
    def test_topic_list(self):
        url = f'/books/subjects/{self.subject.id}/topics/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
    def test_note_creation(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = f'/books/topics/{self.topic.id}/notes/'
        data = {'content': 'Test note content'}
        response = self.client.post(url, data)
        if response.status_code != status.HTTP_201_CREATED:
            print(f"Note creation failed: {response.status_code}, {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Note.objects.filter(user=self.user).exists())
