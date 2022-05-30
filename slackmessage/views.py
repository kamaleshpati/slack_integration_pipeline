import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import slack

from slackmessage.serializer import UserSerializer, MessageSerializer
from slackmessage.serilize_utils import serialize_userinfo, serialize_messageinfo, get_all_message

SLACK_VERIFICATION_TOKEN = getattr(settings, 'VERIFICATION_TOKEN', None)
SLACK_BOT_USER_TOKEN = getattr(settings, 'BOT_USER_ACCESS_TOKEN', None)
Client = slack.WebClient(SLACK_BOT_USER_TOKEN)
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
env = os.environ.get('env')

class Events(APIView):
    def post(self, request, *args, **kwargs):

        slack_message = request.data

        # failed response
        if env != "test" and slack_message.get('token') != SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        # verification
        if slack_message.get('type') == 'url_verification':
            return Response(data=slack_message,
                            status=status.HTTP_200_OK)
        # bot
        if 'event' in slack_message:
            event_message = slack_message.get('event')

            # ignore bot's own message
            if event_message.get('subtype') == 'bot_message':
                return Response(status=status.HTTP_200_OK)

            # process user's message
            user: str = event_message.get('user')
            channel: str = event_message.get('channel')
            bot_text: str = 'Hi <@{}>'.format(user)

            user: UserSerializer = serialize_userinfo(Client, user)

            if len(user.errors) == 0:
                message: MessageSerializer = serialize_messageinfo(event_message, user.data['username'])

            Client.chat_postMessage(method='chat.postMessage',
                                    channel=channel,
                                    text=bot_text + " " + str(user.data))


            return Response(status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_200_OK)


class Messages(APIView):
    def post(self, request, *args, **kwargs):
        slack_message = request.data
        if slack_message.get('token') != SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        res = get_all_message(slack_message["user_id"])

        Client.chat_postMessage(method='chat.postMessage',
                                channel=slack_message.get('channel_id'),
                                text=res)

        return Response(status=status.HTTP_200_OK)


class FilesOperation(APIView):
    def post(self, request, *args, **kwargs):
        slack_message = request.data
        if slack_message.get('token') != SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        file_ = open("/code/asset/" + slack_message["text"], "r")

        Client.api_call("files.upload",
                        files={'file': file_.buffer},
                        data={'channels': slack_message.get('channel_id'),
                              'filename': file_.name,
                              'title': file_.name})

        return Response(status=status.HTTP_200_OK)
