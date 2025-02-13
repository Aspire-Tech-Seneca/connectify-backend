from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

from mongoengine import connect
import datetime

from accounts.models import UserProfile


# Create a new user profile
@api_view(['POST'])
def create_user_profile(request):

    if request.method == 'POST':
        # Initialize the user_profile with the data received in the request
        user_profile = UserProfile(
            username=request.data.get('username'),
            email=request.data.get('email'),
            password=request.data.get('password'),
            first_name=request.data.get('first_name'),
            last_name=request.data.get('last_name')
            # profile_picture='default.jpg',
            # date_of_birth='1990-01-01',
            # age=(datetime.date.today() - dob).days // 365,
            # gender=gender,
            # location=location,
            # interests=interests,
            # bio='This is my bio',
            # age_range=(20, 30),
            # preferred_genders=['Male', 'Female'],
            # matched_users=[],
            # pending_requests=[],
            # blocked_users=[],
            # last_active=datetime.datetime.now(),
            # language_prefer='English',
            # created_at=datetime.datetime.now()
        )

        # Set the password
        user_profile.set_password(request.data.get('password'))
        # Save the user profile to the database
        user_profile.save()
        return Response({
            'message': 'User created successfully',
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user_profile = UserProfile.objects.get(username=username)
            if user_profile.verify_password(password):
                # request.session['user_id'] = str(user_profile.id)
                return Response({
                    'success': True,
                    'message': 'Login successful',
                    'user_id': str(user_profile.id)
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'message': 'Invalid password'
                }, status=status.HTTP_401_UNAUTHORIZED)
        except UserProfile.DoesNotExist:
            return Response({
                'success': False,
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)