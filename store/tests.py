from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Category, Product


class CatalogueFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="New Books", slug="new-books")
        cls.product = Product.objects.create(title="A Story", category=cls.category, kind=Product.Kind.NEW, description="A lovely story.", price="12.50")

    def test_catalog_shows_database_products_and_filters(self):
        response = self.client.get(reverse("catalog"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A Story")
        filtered = self.client.get(reverse("catalog"), {"category": "new-books"})
        self.assertContains(filtered, "A Story")

    def test_product_detail_is_reachable_from_catalog(self):
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A lovely story.")

    def test_reader_can_register_and_log_in(self):
        response = self.client.post(reverse("register"), {
            "username": "newreader",
            "email": "reader@example.test",
            "password1": "A-strong-demo-password-91",
            "password2": "A-strong-demo-password-91",
        })
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(get_user_model().objects.filter(username="newreader", email="reader@example.test").exists())
        self.assertTrue(self.client.login(username="newreader", password="A-strong-demo-password-91"))
