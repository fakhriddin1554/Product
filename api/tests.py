from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase,URLPatternsTestCase
from rest_framework.test import APIClient
from .models import Category
from django.urls import path, include

class CategoryTests(APITestCase,URLPatternsTestCase):
    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    def test_category_get(self):
        url = reverse('task-cats-list')
        response = self.client.get(url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)

    def test_category_create(self):
        url = reverse('task-cats-list')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
