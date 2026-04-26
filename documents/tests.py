from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User
from documents.models import Document
from django.core.files.uploadedfile import SimpleUploadedFile
import io


class DocumentTest(TestCase):
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

        # Mock document
        self.document = Document.objects.create(
            title='Test Document',
            description='Test Description',
            file_name='test.pdf',
            file_size=1024,
            minio_path='documents/test.pdf',
            status='stored',
            uploaded_by=self.admin
        )

    def get_token(self, username, password):
        response = self.client.post('/api/login/', {
            'username': username,
            'password': password
        })
        return response.data['access']

    def get_mock_file(self):
        return SimpleUploadedFile(
            "test.pdf",
            b"mock pdf content",
            content_type="application/pdf"
        )

    # List Tests
    def test_admin_can_list_documents(self):
        token = self.get_token('admin_test', 'Test1234!')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/documents/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_viewer_can_list_documents(self):
        token = self.get_token('viewer_test', 'Test1234!')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/documents/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_cannot_list_documents(self):
        response = self.client.get('/api/documents/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Retrieve Tests
    def test_viewer_can_retrieve_document(self):
        token = self.get_token('viewer_test', 'Test1234!')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(f'/api/documents/{self.document.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Document')

    # Delete Tests
    def test_admin_can_delete_document(self):
        token = self.get_token('admin_test', 'Test1234!')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(
            f'/api/documents/{self.document.id}/delete/'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_editor_cannot_delete_document(self):
        token = self.get_token('editor_test', 'Test1234!')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(
            f'/api/documents/{self.document.id}/delete/'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_viewer_cannot_delete_document(self):
        token = self.get_token('viewer_test', 'Test1234!')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(
            f'/api/documents/{self.document.id}/delete/'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Filter Tests
    def test_filter_by_status(self):
        token = self.get_token('viewer_test', 'Test1234!')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/documents/?status=stored')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for doc in response.data['results']:
            self.assertEqual(doc['status'], 'stored')

    def test_filter_by_title(self):
        token = self.get_token('viewer_test', 'Test1234!')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/documents/?title=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Pagination Tests
    def test_pagination_exists(self):
        token = self.get_token('viewer_test', 'Test1234!')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/documents/')
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)