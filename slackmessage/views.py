import os
import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import slack

from slackmessage.serializer import UserSerializer, MessageSerializer
from slackmessage.serilize_utils import serialize_userinfo, serialize_messageinfo, get_all_message

SLACK_VERIFICATION_TOKEN = getattr(settings, 'VERIFICATION_TOKEN', None)
SLACK_BOT_USER_TOKEN = getattr(settings, 'BOT_USER_ACCESS_TOKEN', None)
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
env = os.environ.get('env')
Client = slack.WebClient(SLACK_BOT_USER_TOKEN) if env != "test" else None


class Health(APIView):
    def get(self, request):
        return Response(data="hiii",status=status.HTTP_200_OK)

# respond to app_mention messages
class Events(APIView):
    def post(self, request, *args, **kwargs):
        slack_message = request.data

        # failed response
        if slack_message.get('token') != SLACK_VERIFICATION_TOKEN:
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

            if len(user.errors) != 0:
                logging.warn("didnt upserted the info for user")
            message: MessageSerializer = serialize_messageinfo(event_message, user.data['username'])

            if env != "test" and Client is not None:
                try:
                    Client.chat_postMessage(method='chat.postMessage',
                                            channel=channel,
                                            text=bot_text + " " + str(user.data))
                except Exception as e:
                    logging.warn("cant post message")

            return Response(status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_200_OK)


# respond to / command to return all messages
class Messages(APIView):
    def post(self, request, *args, **kwargs):
        slack_message = request.data
        if env != "test" and slack_message.get('token') != SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if env != "test" and Client is not None:
            res = get_all_message(slack_message["user_id"])
            try:
                Client.chat_postMessage(method='chat.postMessage',
                                        channel=slack_message.get('channel_id'),
                                        text=res)
            except Exception as e:
                logging.warn("cant post message")

        return Response(status=status.HTTP_200_OK)


# respond to upload_file / command
class FilesOperation(APIView):
    def post(self, request, *args, **kwargs):
        slack_message = request.data
        if env != "test" and slack_message.get('token') != SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        file_name = slack_message["text"]

        if env != "test" and Client is not None:
            try:
                if file_name == "" or file_name is None:
                    Client.chat_postMessage(method='chat.postMessage',
                                            channel=slack_message.get('channel_id'),
                                            text="no file name is given")
                else:
                    file_ = open("/code/asset/" + file_name, "r")
                    Client.api_call("files.upload",
                                    files={'file': file_.buffer},
                                    data={'channels': slack_message.get('channel_id'),
                                          'filename': file_.name,
                                          'title': file_.name})
            except Exception as e:
                logging.warn("cant post message")

        return Response(status=status.HTTP_200_OK)
