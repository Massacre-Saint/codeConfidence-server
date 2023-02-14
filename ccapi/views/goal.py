"""Module sets up Django Viewset for the class of Goal"""
from datetime import date
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ccapi.models import User, LearnedTech, Goal

class GoalView(ViewSet):
    """Class creates viewset for Goal"""
    def retrieve(self, request, pk):
        """Get method retrieves single Goal instance"""
        try:
            goal = Goal.objects.get(pk=pk)
            serializer = GoalSerializer(goal)

            return Response(serializer.data)

        except Goal.DoesNotExist as ex:

            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Get method lists all Goal instances
        Headers:
            Authorization of user['uid']
        """
        uid = request.META['HTTP_AUTHORIZATION']
        goals = Goal.objects.all()
        goals_by_tech = request.query_params.get('learned_tech')

        if goals_by_tech is not None:

            last_updated_goal = goals.filter(uid__uid = uid).order_by('-last_updated', 'progress')
            serializer = GoalSerializer(last_updated_goal, many=True)

        else:

            return Response({})

        return Response(serializer.data)

class GoalSerializer(serializers.ModelSerializer):
    """Created the serializer for Goal class"""

    class Meta:
        depth = 1
        model = Goal
        fields =  (
          'id',
          'title',
          'learned_tech',
          'uid',
          'last_updated',
          'progress'
        )
