from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .forms import LoginForm
from django.contrib.auth.hashers import make_password
from .models  import Student, Teacher

class AccountTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Student.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com',
            fullName='Test User',
            student_id='testid'
        )

    def test_login_view(self):
        response = self.client.get(reverse('account:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_valid_login(self):
        response = self.client.post(reverse('account:login'), {'id': 'testid', 'password': 'testpassword', 'role':'student'})
        self.assertRedirects(response, reverse('dashboard:dashboard'))
        self.assertTrue(self.client.session['_auth_user_id'])

    def test_invalid_login(self):
        response = self.client.post(reverse('account:login'), {'id': 'invaliduser', 'password': 'invalidpassword', 'role': 'student'})
        self.assertRedirects(response, reverse('account:login'))
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_logout_view(self):
        response = self.client.get(reverse('account:logout'))
        self.assertRedirects(response, reverse('account:login'))
'''

'''