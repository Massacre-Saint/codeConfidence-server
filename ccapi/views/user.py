"""Model sets up Django Viewset for the class User"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers,status
from ccapi.models import User

class UserView(ViewSet):
    """Class creates viewset for User"""
    def list(self, request):
        """Get method retrieves single Topic instance"""
        try:
            uid = request.META['HTTP_AUTHORIZATION']
            topic = User.objects.get(uid=uid)
            serializer = UserSerializer(topic)

            return Response(serializer.data)

        except User.DoesNotExist as ex:

            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self,request,pk):
        """Delete method deletes the instance of 
        User and instances that share the foriegn key"""
        user = User.objects.get(pk=pk)
        user.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

class UserSerializer(serializers.ModelSerializer):
    """Class creates the serializer for User class"""

    class Meta:
        depth = 1
        model = User
        fields = (
          'id',
          'display_name',
          'first_name',
          'last_name',
          'bio',
          'image_url',
          'created_on',
          'is_admin',
          'email',
          'uid'
        )
