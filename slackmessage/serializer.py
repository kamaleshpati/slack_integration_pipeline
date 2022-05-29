from rest_framework import serializers

from slackmessage.models import User, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        db_name = "user"
        model = User
        fields = ['slackuser_id','username','email']

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        db_name = "message"
        model = Message
        fields = ['slackuser_id','message_id','text', 'file', 'timestamp', 'author']

    def create(self, validated_data):
        return Message.objects.create(**validated_data)




