from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User


class UserAuthTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username='admin_test',
            password='Test1234!',
            role='admin'
        )
        self.editor = User.objects.create_user(
            username='editor_test',
            password='Test1234!',
            role='editor'
        )
        self.viewer = User.objects.create_user(
            username='viewer_test',
            password='Test1234!',
            role='viewer'
        )

    def get_token(self, username, password):
        response = self.client.post('/api/login/', {
            'username': username,
            'password': password
        })
        return response.data['access']

    # Login Tests
    def test_login_success(self):
        response = self.client.post('/api/login/', {
            'username': 'admin_test',
            'password': 'Test1234!'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_wrong_password(self):
        response = self.client.post('/api/login/', {
            'username': 'admin_test',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_wrong_username(self):
        response = self.client.post('/api/login/', {
            'username': 'nobody',
            'password': 'Test1234!'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # RBAC Tests
    def test_admin_can_create_user(self):
        token = self.get_token('admin_test', 'Test1234!')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post('/api/users/create/', {
            'username': 'new_user',
            'password': 'Test1234!',
            'role': 'viewer'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_editor_cannot_create_user(self):
        token = self.get_token('editor_test', 'Test1234!')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post('/api/users/create/', {
            'username': 'new_user',
            'password': 'Test1234!',
            'role': 'viewer'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_viewer_cannot_create_user(self):
        token = self.get_token('viewer_test', 'Test1234!')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post('/api/users/create/', {
            'username': 'new_user',
            'password': 'Test1234!',
            'role': 'viewer'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_cannot_create_user(self):
        response = self.client.post('/api/users/create/', {
            'username': 'new_user',
            'password': 'Test1234!',
            'role': 'viewer'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)