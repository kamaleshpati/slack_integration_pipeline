import json
import os
import logging

from django.core import serializers

from slackmessage.models import Message
from slackmessage.serializer import UserSerializer, MessageSerializer

env = os.environ.get('env')


def serialize_userinfo(Client, user_id: str):
    if env == "test":
        userinfo = json.load(open("/code/slackmessage/resources/user.json"))
    else:
        userinfo: dict = Client.users_info(user=user_id)

    user = dict()
    user['slackuser_id'] = userinfo['user'].get("id")
    user['username'] = userinfo['user'].get("real_name")
    user['email'] = userinfo['user']['profile'].get("email")
    user: UserSerializer = UserSerializer(data=user, partial=True)
    if user.is_valid():
        user.save()
    else:
        logging.warn(user.errors)
    return user


def serialize_messageinfo(event_message: dict, author: str):
    message = dict()
    message['message_id'] = event_message['client_msg_id']
    message['slackuser_id'] = event_message['user']
    message['author'] = author
    message['text'] = event_message['text']
    message['timestamp'] = event_message['event_ts']
    message: MessageSerializer = MessageSerializer(data=message, partial=True)
    if message.is_valid():
        message.save()
    else:
        logging.warn(message.errors)

    return message


def get_all_message(user_id: str):
    res = Message.objects.filter(slackuser_id=user_id)
    return serializers.serialize("json", res)
