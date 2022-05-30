import json
from unittest.mock import MagicMock
from django.urls import reverse

from rest_framework.test import APITestCase

from slackmessage import serilize_utils
from slackmessage.models import User, Message


class EventsAPIViewTestCase(APITestCase):

    def test_channel_msg(self):
        url = reverse("slackmessage:event")
        data = open("/code/slackmessage/resources/message.json")
        serilize_utils.fetch_user = MagicMock(return_value=json.load(open("/code/slackmessage/resources/user.json")))
        response = self.client.post(url, json.load(data), format="json")
        self.assertEqual(200, response.status_code)

        # user exits
        user = User.objects.filter(slackuser_id="U033Q99808Y")
        self.assertIsNotNone(user)

        # message exists
        message = Message.objects.filter(slackuser_id="U033Q99808Y")
        self.assertIsNotNone(message)



    def test_channel_slash(self):
        url = reverse("slackmessage:message")
        data = open("/code/slackmessage/resources/slash_command_message.json")
        response = self.client.post(url, json.load(data), format="json")
        self.assertEqual(200, response.status_code)

