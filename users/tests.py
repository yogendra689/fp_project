from rest_framework.test import APITestCase
from users.models import Post
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from django.core.files.uploadedfile import SimpleUploadedFile
import os

User = get_user_model()


class PostApiViewTest(APITestCase):
    """ Test module for GET all puppies API """

    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='foobar',
            email='foo@bar.com',
            password='barbaz',
            is_staff=True,
            id=1
        )
        self.normal_user = User.objects.create_user(
            username='foobar2',
            email='foo2@bar.com',
            password='barbaz',
            id=2
        )
        self.post1 = Post.objects.create(
            title='Casper', body='test lorem ipsum', user=self.admin_user)
        self.post2 = Post.objects.create(
            title='Lorem', body='test lorem ipsum', user=self.normal_user)

        self.admin_creds = {'username': 'foobar', 'password': 'barbaz'}
        self.normal_user_creds = {'username': 'foobar2', 'password': 'barbaz'}

    def test_get_posts_for_superuser(self):
        url = reverse('token_obtain_pair')
        resp = self.client.post(url, self.admin_creds, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        token = resp.data['access']

        url = reverse('user_posts')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        resp = self.client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data['data']), 2)

    def test_get_posts_for_normal_user(self):
        url = reverse('token_obtain_pair')
        resp = self.client.post(url, self.normal_user_creds, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        token = resp.data['access']

        url = reverse('user_posts')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        resp = self.client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data['data']), 1)
        self.assertEqual(resp.data['data'][0]['id'], self.post2.id)

    def test_upload_posts_for_admin_user(self):
        url = reverse('token_obtain_pair')
        resp = self.client.post(url, self.normal_user_creds, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('user_posts')

        with open(os.path.join(os.path.dirname(__file__), 'fixtures/test_img.png'), 'rb') as img:
            resp = self.client.post(url, {'file': img})
            self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
            self.assertEqual(resp.data['data'], 'invalid file')

        with open(os.path.join(os.path.dirname(__file__), 'fixtures/invalid_test_data.json'), 'rb') as json_data:
            resp = self.client.post(url, {'file': json_data})
            self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
            self.assertEqual(resp.data['data'], 'invalid file')

        with open(os.path.join(os.path.dirname(__file__), 'fixtures/invalid_test_data_two.json'), 'rb') as json_data:
            resp = self.client.post(url, {'file': json_data})
            self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        with open(os.path.join(os.path.dirname(__file__), 'fixtures/valid_test_data.json'), 'rb') as json_data:
            resp = self.client.post(url, {'file': json_data})
            self.assertEqual(resp.status_code, status.HTTP_200_OK)
            self.assertEqual(Post.objects.count(), 3)
            self.assertEqual(resp.data['data'], 'records saved')
