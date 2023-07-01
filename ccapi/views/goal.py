"""Module sets up Django Viewset for the class of Goal"""
from datetime import date
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
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

    @action(detail=False)
    def filter(self,request):
        goals = Goal.objects.all()
        uid = request.META['HTTP_AUTHORIZATION']
        l_tech = request.query_params.get('l_tech')
        last_updated = request.query_params.get('last_updated')
        a_z = request.query_params.get('alpha')
        z_a = request.query_params.get('zeta')
        goals_by_tech = goals.filter(learned_tech = l_tech, uid__uid = uid)
        progress = request.query_params.get('progress')
        if progress is not None:
            if progress == '25':
                goals_by_tech = goals_by_tech.order_by('progress')
            if progress == '50':
                goals_by_tech = goals_by_tech.order_by('-progress')
        if last_updated is not None:
            goals_by_tech = goals_by_tech.order_by('-last_updated')
        if a_z is not None:
            goals_by_tech = goals_by_tech.order_by('title')
        if z_a is not None:
            goals_by_tech = goals_by_tech.order_by('-title')
        serializer = GoalSerializer(goals_by_tech, many=True)
        return Response(serializer.data)
    
    @action(detail=False)
    def all_filter(self,request):
        topics = Goal.objects.all()
        uid = request.META['HTTP_AUTHORIZATION']
        last_updated = request.query_params.get('last_updated')
        a_z = request.query_params.get('alpha')
        z_a = request.query_params.get('zeta')
        goals_by_user = topics.filter(uid__uid = uid)
        progress = request.query_params.get('progress')
        
        if progress is not None:
            if progress == '25':
                goals_by_user = goals_by_user.order_by('progress')
            if progress == '50':
                goals_by_user = goals_by_user.order_by('-progress')
        if last_updated is not None:
            goals_by_user = goals_by_user.order_by('last_updated')
        if a_z is not None:
            goals_by_user = goals_by_user.order_by('title')
        if z_a is not None:
            goals_by_user = goals_by_user.order_by('-title')

        serializer = GoalSerializer(goals_by_user, many=True)
        return Response(serializer.data)
    
    def list(self, request):
        """Get method lists all Goal instances
        Headers:
            Authorization of user['uid']
        Params:
          'learned_tech' : id
        """
        uid = request.META['HTTP_AUTHORIZATION']
        goals = Goal.objects.all()
        user_goals = goals.filter(uid__uid = uid)
        l_tech_param = request.query_params.get('l_tech')

        if l_tech_param is not None:
            goals_by_param = goals.filter(learned_tech = l_tech_param, uid__uid = uid)
            ordered_goals = goals_by_param.order_by('-last_updated', 'progress')
            serializer = GoalSerializer(ordered_goals, many=True)

        else:
            try:
                serializer = GoalSerializer(user_goals, many=True)

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
