from django.core.urlresolvers import reverse
from django.test import TestCase

from interface.models import Result


class ResultTests(TestCase):
    def setUp(self):
        self.result = Result.objects.create(
            text = 'Hello world'
        )

    def test_get_result_detail_200(self):
        url = reverse('result_detail', kwargs={'pk': self.result.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_result_detail_404(self):
        url = reverse('result_detail', kwargs={'pk': self.result.id+1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class WebhookTests(TestCase):
    def setUp(self):
        self.data = {}

    def test_post_webhook_200(self):
        url = reverse('webhook')
        response = self.client.post(url, data=self.data)
        self.assertEqual(response.status_code, 204)
