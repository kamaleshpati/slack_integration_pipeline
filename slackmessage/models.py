from django.db import models


class User(models.Model):
    slackuser_id = models.CharField(max_length=100, primary_key=True)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)


class Message(models.Model):
    message_id = models.CharField(max_length=300, primary_key=True, null=False, default="1")
    slackuser_id = models.CharField(max_length=300)
    text = models.CharField(max_length=300, default="")
    file = models.CharField(max_length=300, default="")
    timestamp = models.CharField(max_length=100)
    author = models.CharField(max_length=30)
