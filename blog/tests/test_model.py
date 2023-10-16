from django.test import TestCase
from blog.models import Category

class CategoryTest(TestCase):
    def test_create_category(self):
        category = Category.objects.create(
            name="TEST_NAME",
            slug="TEST_SLUG" 
        )
        self.assertEqual(str(category), "TEST_NAME")
        self.assertEqual(category.slug, "TEST_SLUG")
        self.assertIsInstance(category, Category)