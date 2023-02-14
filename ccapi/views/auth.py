"""This module handles Google's authication using 
Firebase and Post/Get's an instance of User Class"""
from ccapi.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import date


@api_view(['POST'])
def check_user(request):
    '''Checks to see if logged in User has Associated User Model

    Method arguments:
      request -- The full HTTP request object
    '''
    uid = request.data['uid']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    user = User.objects.filter(uid=uid).first()

    # If authentication was successful, respond with their token
    if user is not None:
        data = {
            'id': user.id,
            'display_name': user.display_name,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'bio': user.bio,
            'image_url': user.image_url,
            'created_on': user.created_on,
            'is_admin': user.is_admin,
            'email': user.email,
            'uid': user.uid
        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = { 'valid': False }
        return Response(data)


@api_view(['POST'])
def register_user(request):
    '''Handles the creation of a new User for authentication

    Method arguments:
      request -- The full HTTP request object
    '''
    users = User.objects.all()

    # Now save the user info in the ccapi_User table
    user = User.objects.create(
        display_name = request.data['display_name'],
        first_name = request.data['first_name'],
        last_name = request.data['last_name'],
        bio = request.data['bio'],
        image_url = request.data['image_url'],
        created_on = date.today(),
        is_admin = True if len(users) < 1 else False,
        email = request.data['email'],
        uid = request.data['uid']
    )

    # Return the user info to the client
    data = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'bio': user.bio,
        'image_url': user.image_url,
        'created_on': user.created_on,
        'is_admin': user.is_admin,
        'email': user.email,
        'uid': user.uid
    }
    return Response(data)
