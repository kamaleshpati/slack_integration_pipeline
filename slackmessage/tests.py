import json

from django.urls import reverse

from rest_framework.test import APITestCase


class EventsAPIViewTestCase(APITestCase):
    url = reverse("slackmessage:event")

    def test(self):
        """
        Test to verify that a post call with invalid passwords
        """
        data = open("/code/slackmessage/resources/message.json")
        response = self.client.post(self.url, json.load(data), format="json")
        self.assertEqual(200, response.status_code)
