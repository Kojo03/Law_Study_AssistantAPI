from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from accounts.models import User
from books.models import Subject, Topic
from .models import Case

class CaseModelTest(TestCase):
    def setUp(self):
        self.subject = Subject.objects.create(
            title='Criminal Law',
            description='Study of criminal law principles'
        )
        self.topic = Topic.objects.create(
            subject=self.subject,
            title='Murder Cases'
        )
        
    def test_case_creation(self):
        case = Case.objects.create(
            topic=self.topic,
            title='R v Smith',
            summary='Important murder case',
            citation='[2023] UKHL 1',
            year=2023
        )
        self.assertEqual(case.title, 'R v Smith')
        self.assertEqual(case.topic, self.topic)
        self.assertEqual(str(case), 'R v Smith')

class CasesAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        
        self.subject = Subject.objects.create(
            title='Criminal Law'
        )
        self.topic = Topic.objects.create(
            subject=self.subject,
            title='Murder Cases'
        )
        self.case = Case.objects.create(
            topic=self.topic,
            title='R v Smith',
            summary='Important murder case'
        )
        
    def test_case_list(self):
        url = f'/cases/topics/{self.topic.id}/cases/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
    def test_case_detail(self):
        url = reverse('case-detail', kwargs={'pk': self.case.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'R v Smith')
