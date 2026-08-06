from django.test import Client, TestCase
from django.urls import reverse


class SmokeTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_redirects_to_blog(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('/blog/'))

    def test_blog_index(self):
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)

    def test_polls_index(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get(reverse('user_manager:login'))
        self.assertEqual(response.status_code, 200)
