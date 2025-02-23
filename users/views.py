from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt

from users.models import UserProfile
from users.serializers import UserProfileSerializer

import logging

logger = logging.getLogger(__name__)


@csrf_exempt  # Use with extreme caution in production!
@api_view(['POST'])
def create_user_profile(request):
    """
    Create a new user profile.
    """
    if request.method == 'POST':
        serializer = UserProfileSerializer(data=request.data)

        if serializer.is_valid():
            # Save the new user profile and return success response
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # If the serializer is not valid, return error response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt  # Use with extreme caution in production!
@api_view(['POST'])
def user_login(request):
    """
    API to login a user and get a JWT token using email and password.
    """
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate using email and password
        user = authenticate(username=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        

@csrf_exempt  # Use with extreme caution in production!
@api_view(['POST'])
def user_logout(request):
    """
    API to logout the user by blacklisting the refresh token.
    """
    if request.method == 'POST':
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the refresh token to prevent future usage
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print(e)
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt  # Use with extreme caution in production!
@api_view(['PUT'])
def update_user_profile(request):
    """
    API to update the user's profile information.
    """
    if request.method == 'PUT':
        user = request.user   # Get the current user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            print(f"Current user data: {user}")
            print(f"Updated user data: {serializer.validated_data}")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# Delete user profile
@csrf_exempt  # Use with extreme caution in production!
@api_view(['DELETE'])
def delete_user_profile(request):
    """
    API to delete the user's profile .
    """
    if request.method == 'DELETE':
        user = request.user
        user.delete()   # Delete the user profile
        return Response({"detail": "User profile deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
