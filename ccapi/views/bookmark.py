"""Module sets up Djnago Viewset for the class of Bookmark"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ccapi.models import Bookmark, User, Resource
from django.db import IntegrityError

class BookmarkView(ViewSet):
    """Class creates the viewset for Bookmark class"""
    def list(self, request):
        """Get method get list of all Bookmark instances"""
        bookmarks = Bookmark.objects.all()
        sorted_by_parent = sorted(bookmarks, key=lambda x: (x.parent_id))
        serializer = BookmarkSerilaizer(sorted_by_parent, many=True)

        return Response(serializer.data)

    def create(self, request):
        """Post method creates one or more bookmarks from JSON data"""
        body = request.data
        bookmarks = Bookmark.objects.all()

        try:
            if (body['title'] == 'Code Confidence Resources'):
                create_bookmark_children(body)
            parent_bookmarks = bookmarks.filter(id=body['parentId'])
            if len(parent_bookmarks) == 0 and body['title'] != 'Code Confidence Resources':
                return Response({'error': 'Parent bookmark does not exist'}, status=status.HTTP_404_NOT_FOUND)
            else:
                bookmark = create_bookmark_children(body)
                serializer = BookmarkSerilaizer(bookmark)

                return Response(serializer.data)

        except IntegrityError:
            # If a UNIQUE constraint error occurs, return a 409 Conflict response
            return Response({'error': 'Bookmark with this id already exists'}, status=status.HTTP_409_CONFLICT)

    def update(self, request, pk):
        """Put method updates instance of bookmark"""
        body = request.data
        bookmark = Bookmark.objects.get(pk=pk)
        bookmark.index = body['index']
        bookmark.parent_id = body['parent_id']
        bookmark.title = body['title']
        if 'url' in body:
            bookmark.url = body['url']
        update_bookmark_children(body, pk)
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Delete method deletes the instance and children of pk"""
        bookmark = Bookmark.objects.get(pk=pk)
        body= request.data
        bookmarks = Bookmark.objects.all()
        resources = Resource.objects.all()
        try:
            if bookmark.title == 'Code Confidence Resources':
                bookmarks.delete()
                resources.delete()
        except:
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        
        try:
            for index in resources:
                if bookmark.id == index.bookmark_id:
                    index.delete()
        except:
            return Response({'error': 'Resource does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            children = Bookmark.objects.filter(parent_id = bookmark.id)
            if children is not None:
                bookmark.delete()
                delete_bookmark_children(children,bookmarks)
            else:
                bookmark.delete()
                pass

        except:
            return Response(None, status=status.HTTP_204_NO_CONTENT)
                    
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class BookmarkSerilaizer(serializers.ModelSerializer):
    """Class creates the serializer for BookMark class"""
    class Meta:
        depth = 1
        model = Bookmark
        fields = (
          'id',
          'index',
          'parent_id',
          'title',
          'url',
        )

def create_bookmark_children(json_data):
    # create or retrieve the parent bookmark
    bookmark, created = Bookmark.objects.get_or_create(
        id=int(json_data['id']),
        defaults={
            'index': json_data['index'],
            'parent_id': int(json_data['parentId']),
            'title': json_data['title'],
            'url': json_data.get('url', None),
        },
    )

    # recursively create child bookmarks
    if 'children' in json_data:
        for child_data in json_data['children']:
            create_bookmark_children(child_data)

    return bookmark
    
def update_bookmark_children(body, pk):
    #fetch and update bookmark
    bookmark, created = Bookmark.objects.update_or_create(
        id= int(pk),
        defaults={
            'index': body['index'],
            'parent_id': int(body['parent_id']),
            'title': body['title'],
            'url': body.get('url', None),
        },
    )
    
    if 'children' in body:
        for child_data in body['children']:
            update_bookmark_children(child_data)

    return bookmark
 
        
def delete_bookmark_children(parents,bookmarks):
    deleted_children = []
    for bookmark in parents:
        try:
            children = bookmarks.filter(parent_id = bookmark.id)
            deleted_children.append(children)
            if children is not None:
                delete_bookmark_children(children, bookmarks)
            else:
                pass
        except:
            pass
    parents.delete()
    deleted_children.delete()
    return Response("Children deleted successfully")
