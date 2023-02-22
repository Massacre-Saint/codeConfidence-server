"""Module sets up Django Viewset for the class of Tech"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from ccapi.models import Tech, LearnedTech

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
        if 'Authorization' in request.headers:
            uid = request.META['HTTP_AUTHORIZATION']
            learned_tech = LearnedTech.objects.filter(uid_id__uid=uid)
            user_tech = learned_tech.filter(uid_id__uid=uid)

            if len(user_tech) > 0:
                learned_tech_ids = [u.tech.id for u in user_tech]
                final = tech.exclude(id__in=learned_tech_ids)
            else:
                final = tech

            serializer = TechSerializer(final, many=True)
            return Response(serializer.data)
            
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
