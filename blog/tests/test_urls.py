from django.test import TestCase
from django.urls import reverse


class URLTest(TestCase):
    def test_post_list_page(self):
        response = self.client.get(reverse("posts-list"))
        self.assertEqual(response.status_code, 200)