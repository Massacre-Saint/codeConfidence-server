"""Module sets up Django Viewset for the class of Topic"""
from datetime import date
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ccapi.models import Goal, User, LearnedTech, Topic


class TopicView(ViewSet):
    """Class creates viewset for Topic"""
    def retrieve(self, request, pk):
        """Get method retrieves single Topic instance"""
        try:
            topic = Topic.objects.get(pk=pk)
            serializer = TopicSerializer(topic)

            return Response(serializer.data)

        except Topic.DoesNotExist as ex:

            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Get method lists all Topic instances
        Headers:
            Authorization of user['uid']
        Params:
          'learned_tech' : id
        """
        uid = request.META['HTTP_AUTHORIZATION']
        topics = Topic.objects.all()
        l_tech_param = request.query_params.get('learned_tech')
        goal_param = request.query_params.get('goal')

        if l_tech_param  and goal_param is not None:
            topics_by_goal = topics.filter(learned_tech = l_tech_param, uid__uid = uid)
            ordered_topics = topics_by_goal.order_by('-last_updated', '-completed')
            serializer = TopicSerializer(ordered_topics, many=True)

        else:
            try:
                serializer = TopicSerializer(topics, many=True)

                return Response(serializer.data)

            except Topic.DoesNotExist:

                return Response({})

        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)

    def create(self,request):
        """Post method created an instance of Topic
        Headers:
        Authorization of user['uid']"""
        body = request.data
        uid = request.META['HTTP_AUTHORIZATION']

        l_tech = LearnedTech.objects.get(pk=body['learned_tech'])
        user = User.objects.get(uid=uid)


        if 'goal' in body:
            goal = Goal.objects.get(pk=body['goal'])
            topic = Topic.objects.create(
              title=body['title'],
              description=body['description'],
              uid=user,
              learned_tech=l_tech,
              goal=goal,
              last_updated = date.today(),
              completed = body['completed'],
            )
            
            serializer = TopicSerializer(topic)
        else:
            topic = Topic.objects.create(
              title=body['title'],
              description=body['description'],
              uid=user,
              learned_tech=l_tech,
              last_updated = date.today(),
              completed = body['completed'],
            )
            serializer = TopicSerializer(topic)
        return Response(serializer.data)

    def update(self, request, pk):
        """Put method updates instance of topic"""
        body = request.data
        l_tech = LearnedTech.objects.get(pk=body['learned_tech'])
        topic = Topic.objects.get(pk=pk)

        if 'goal' in body:
            goal = Goal.objects.get(pk=body['goal'])
            topic.title = body['title']
            topic.description = body['description']
            topic.learned_tech = l_tech
            topic.goal = goal
            topic.last_updated = date.today()
            topic.completed = body['completed']
            topic.save()
        else:
            topic.title = body['title']
            topic.description = body['description']
            topic.learned_tech = l_tech
            topic.last_updated = date.today()
            topic.completed = body['completed']
            topic.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self,request,pk):
        """Delete method deletes the instance of 
        Topic and instances that share the foriegn key"""
        topic = Topic.objects.get(pk=pk)
        topic.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

class TopicSerializer(serializers.ModelSerializer):
    """Class creates the serializer for Topic class"""

    class Meta:
        depth = 1
        model = Topic
        fields = (
          'id',
          'title',
          'description',
          'uid',
          'learned_tech',
          'goal',
          'last_updated',
          'completed'
        )
