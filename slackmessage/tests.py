import json

from django.urls import reverse

from rest_framework.test import APITestCase


class EventsAPIViewTestCase(APITestCase):

    def test_channel_msg(self):
        """
        Test to verify that a post call with invalid passwords
        """
        url = reverse("slackmessage:event")
        data = open("/code/slackmessage/resources/message.json")
        response = self.client.post(url, json.load(data), format="json")
        self.assertEqual(200, response.status_code)


    def test_channel_slash(self):
        url = reverse("slackmessage:message")
        data = open("/code/slackmessage/resources/slash_command_message.json")
        response = self.client.post(url, json.load(data), format="json")
        self.assertEqual(200, response.status_code)
