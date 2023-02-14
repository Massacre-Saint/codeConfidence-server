"""Module sets up Django Viewset for the class of Message"""
from random import randrange
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from ccapi.models import Message

class MessageView(ViewSet):
    """Class creates the Viewset for class Message"""

    def list(self, request):
        """Method GETs single random message instance"""
        count = Message.objects.count()
        random_index = randrange(count)
        random_message = Message.objects.all()[random_index]
        serializer = MessageSerializer(random_message)

        return Response(serializer.data)
class MessageSerializer(serializers.ModelSerializer):
    """Class creates the serializer for Message class"""

    class Meta:
        model = Message
        fields = (
          'id',
          'title',
          'author'
          )
