"""Module sets up Django Viewset for the class of Goal"""
from datetime import date
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ccapi.models import User, LearnedTech, Goal, Topic

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
        Params:
          'learned_tech' : id
        """
        uid = request.META['HTTP_AUTHORIZATION']
        goals = Goal.objects.all()
        l_tech_param = request.query_params.get('l_tech')

        if l_tech_param is not None:
            goals_by_param = goals.filter(learned_tech = l_tech_param, uid__uid = uid)
            ordered_goals = goals_by_param.order_by('-last_updated', 'progress')
            serializer = GoalSerializer(ordered_goals, many=True)

        else:
            try:
                serializer = GoalSerializer(goals, many=True)

                return Response(serializer.data)

            except Goal.DoesNotExist:

                return Response({})

        return Response(serializer.data)

    def create(self, request):
        """Post method created an instance of Goal
        Headers:
            Authorization of user['uid']
        """
        body = request.data
        uid = request.META['HTTP_AUTHORIZATION']
        user = User.objects.get(uid=uid)
        l_tech = LearnedTech.objects.get(pk=body['learned_tech'])

        goal = Goal.objects.create(
          title = body['title'],
          learned_tech = l_tech,
          uid = user,
          last_updated = date.today(),
        )
        serializer = GoalSerializer(goal)

        return Response(serializer.data)

    def update(self, request, pk):
        """Put methods updates instance Goal"""
        body=request.data
        goal=Goal.objects.get(pk=pk)
        uid = request.META['HTTP_AUTHORIZATION']
        user = User.objects.get(uid=uid)
        l_tech = LearnedTech.objects.get(pk=body['learned_tech'])

        goal.title = body['title']
        goal.last_updated = date.today()
        goal.learned_tech = l_tech
        goal.uid = user

        #logic for progress field
        topics = Topic.objects.filter(goal = goal.pk).count()
        print('this is on goal')
        if topics > 0:
            completed_topics = Topic.objects.filter(completed=True, goal = goal.pk).count()
            progress = completed_topics / topics * 100
            goal.progress = progress
        else:
            goal.progress = None
        goal.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self,request,pk):
        """Delete method deletes the instance of 
        Goal and instances that share the foriegn key"""
        goal = Goal.objects.get(pk=pk)
        goal.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

class GoalSerializer(serializers.ModelSerializer):
    """Created the serializer for Goal class"""

    class Meta:
        depth = 2
        model = Goal
        fields =  (
          'id',
          'title',
          'learned_tech',
          'uid',
          'last_updated',
          'progress'
        )
