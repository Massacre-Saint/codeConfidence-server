"""Module sets up Djnago Viewset for the class of Resource"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ccapi.models import Bookmark, Resource,LearnedTech, Topic, Goal
from django.db import IntegrityError
from django.contrib.contenttypes.models import ContentType

class ResourceView(ViewSet):
    """Class creates the viewset for Resource Class"""
    def list(self, request):
        """Get method gets list of all Resource instances"""
        resources = Resource.objects.all()
        serializer = ResourceSerilaizer(resources, many=True)

        return Response(serializer.data)

    def create(self, request):
        """Post method creates one or more bookmarks from JSON data"""
        body = request.data
        bookmark = Bookmark.objects.get(pk=body['bookmark'])
        bookmarks = Bookmark.objects.all()
        tech = LearnedTech.objects.get(pk=body['tech'])
        
        if 'assignedTo' in body and body['assignedTo'] is not None:
          resource_id = body['assignedTo']
          topics = Topic.objects.filter(id=resource_id)
          goals = Goal.objects.filter(id=resource_id)
          if topics.exists():
                assigned_to = ContentType.objects.get_for_model(topics.first())
                object_id = topics.first().id
          elif goals.exists():
              assigned_to = ContentType.objects.get_for_model(goals.first())
              object_id = goals.first().id

          resource = Resource.objects.create(
            bookmark = bookmark,
            assigned_to = assigned_to,
            object_id = object_id,
            tech = tech,
          )
        else:
          resource = Resource.objects.create(
            bookmark = bookmark,
            assigned_to = None,
            tech = tech,
          )
        try:
          resource = create_resource_children(resource, bookmarks)
          
        except IntegrityError:

          return Response({'error': 'Resource has no children'})

        serializer = ResourceSerilaizer(resource)
        return  Response(serializer.data)
    
    def update(self, request, pk):
        """Update method updates an instance and children data"""
        resource = Resource.objects.get(pk=pk)
        body = request.data
        bookmarks = Bookmark.objects.all()
        bookmark = Bookmark.objects.get(pk=body['bookmark'])
        tech = LearnedTech.objects.get(pk=body['tech'])
        
        resource.tech = tech
        if 'assignedTo' in body and body['assignedTo'] is not None:
            resource_id = body['assignedTo']
            topics = Topic.objects.filter(id=resource_id)
            goals = Goal.objects.filter(id=resource_id)
            if topics.exists():
                assigned_to = ContentType.objects.get_for_model(topics.first())
                object_id = topics.first().id
            elif goals.exists():
                assigned_to = ContentType.objects.get_for_model(goals.first())
                object_id = goals.first().id

            resource.assigned_to = assigned_to
            resource.object_id = object_id
        else:
            resource.assigned_to = None
            resource.object_id = None

        try:
            resource = update_resource_children(resource, bookmarks, body)
        except IntegrityError:
            return Response({'error': 'Resource has no children'})

        resource.save()
        serializer = ResourceSerilaizer(resource)
        return Response(serializer.data)

    def destroy(self, request, pk):
        """Delete method deletes the instance and children of pk"""
        resource = Resource.objects.get(pk=pk)
        resources = Resource.objects.all()
        children= resources.filter(bookmark_id__parent_id = resource.bookmark_id)
        if len(children) > 0:
          children.delete()
        resource.delete()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)
  
class ResourceSerilaizer(serializers.ModelSerializer):
    """Class creates the serializer for BookMark class"""
    class Meta:
        depth = 1
        model = Resource
        fields = (
          'id',
          'bookmark',
          'object_id',
          'tech',
        )

def create_children_from_bookmark(resource,bookmark):
    book = Bookmark.objects.get(pk=bookmark.id)
    lTech = LearnedTech.objects.get(pk=resource.tech_id)
    resource, created = Resource.objects.get_or_create(
        bookmark=book,
        assigned_to=resource.assigned_to,
        object_id = resource.object_id,
        tech=lTech,
    )
    return resource

def create_resource_children(resource, bookmarks):
    children = bookmarks.filter(parent_id=resource.bookmark_id)
    if len(children) > 0:
        for child in children:
            child_resource = create_children_from_bookmark(resource,child)
            child_resource.save()
            create_resource_children(child_resource, bookmarks)

def update_children_from_bookmark(resource, bookmark):
    book = Bookmark.objects.get(pk=bookmark.id)
    lTech = LearnedTech.objects.get(pk=resource.tech_id)
    resource, created = Resource.objects.get_or_create(
        bookmark=book,
        assigned_to=resource.assigned_to,
        object_id=resource.object_id,
        tech=lTech,
    )
    return resource

def update_resource_children(resource, bookmarks, body):
    children = bookmarks.filter(parent_id=resource.bookmark_id)
    if len(children) > 0:
        for child in children:
            child_resource = Resource.objects.filter(bookmark=child).first()
            if child_resource:
                if 'tech' in body:
                    child_resource.tech = LearnedTech.objects.get(pk=body['tech'])

                if 'assignedTo' in body and body['assignedTo'] is not None:
                    resource_id = body['assignedTo']
                    topics = Topic.objects.filter(id=resource_id)
                    goals = Goal.objects.filter(id=resource_id)
                    if topics.exists():
                        assigned_to = ContentType.objects.get_for_model(topics.first())
                        object_id = topics.first().id
                    elif goals.exists():
                        assigned_to = ContentType.objects.get_for_model(goals.first())
                        object_id = goals.first().id

                    child_resource.assigned_to = assigned_to
                    child_resource.object_id = object_id
                else:
                    child_resource.assigned_to = None
                    child_resource.object_id = None

                child_resource.save()
                update_resource_children(child_resource, bookmarks, body)
            else:
                child_resource = update_children_from_bookmark(resource, child)
                child_resource.save()
                update_resource_children(child_resource, bookmarks, body)

    return resource
