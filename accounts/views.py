from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

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

        user_profile.save()
        return Response({
            'message': 'User created successfully',
        }, status=status.HTTP_201_CREATED)


