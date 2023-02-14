"""Module sets up Django Viewset for the class of Tech"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from ccapi.models import Tech

class TechView(ViewSet):
    """Class creates viewset for Tech"""
    def retrieve(self, request, pk):
        """Get method retrieves single Tech instance"""
        tech = Tech.objects.get(pk=pk)
        serializer = TechSerializer(tech)

        return Response(serializer.data)

    def list(self, request):
        """Get method lists all Tech instances"""
        tech = Tech.objects.all()
        serializer = TechSerializer(tech, many=True)

        return Response(serializer.data)

class TechSerializer(serializers.ModelSerializer):
    """Class creates the serializer for Tech class"""

    class Meta:
        model = Tech
        fields = (
          'id',
          'name',
          'description',
          'doc_url',
          'image_url',
        )
