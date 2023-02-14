"""Module sets up Django Viewset for the class of LearnedTech"""
from datetime import date
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ccapi.models import Tech, User, LearnedTech

class LearnedTechView(ViewSet):
    """Class creates viewset for LeanredTech"""
    def retrieve(self, request, pk):
        """Get method retrieves single LearnedTech instance"""
        try:
            learned_tech = LearnedTech.objects.get(pk=pk)
            serializer = LearnedTechSerializer(learned_tech)

            return Response(serializer.data)

        except LearnedTech.DoesNotExist as ex:

            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Get method lists all LearnedTech instances
        Headers:
            Authorization of user['uid']
        """
        uid = request.META['HTTP_AUTHORIZATION']

        learned_tech = LearnedTech.objects.all()
        last_updated_tech = learned_tech.filter(uid__uid = uid).order_by('-last_updated')
        serializer = LearnedTechSerializer(last_updated_tech, many=True)

        return Response(serializer.data)

    def create(self, request):
        """Post Method creates an instance of LearnedTech
        Args:
            request: object
        Headers:
            Authorization of user['uid']
        Body:
            takes only tech: pk
        """
        body = request.data
        uid = request.META['HTTP_AUTHORIZATION']
        user = User.objects.get(uid=uid)
        tech = Tech.objects.get(pk=body['tech'])

        learned_tech = LearnedTech.objects.create(
          uid = user,
          tech = tech,
          last_updated = date.today()
        )

        serializer = LearnedTechSerializer(learned_tech)

        return Response(serializer.data)

    def update(self, request, pk):
        """Put method updates an instance of LearnedTech
        Args:
            request: object
            pk: l_tech['id']
        Body:
            {'id', 'tech': tech['id']}
        """
        body = request.data
        l_tech = LearnedTech.objects.get(pk = pk)
        tech = Tech.objects.get(pk=body['tech'])
        # UX might allow to change learned_tech in future, leaving functionality for now
        l_tech.tech = tech
        l_tech.last_updated = date.today()
        l_tech.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Delete method deletes the instance of 
        LearnedTech and instances that share the foreign key"""
        learned_tech = LearnedTech.objects.get(pk=pk)
        learned_tech.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

class LearnedTechSerializer(serializers.ModelSerializer):
    """Class creates the serializer for LearnedTech class"""

    class Meta:
        depth = 1
        model = LearnedTech
        fields = (
          'uid',
          'tech',
          'last_updated'
        )
