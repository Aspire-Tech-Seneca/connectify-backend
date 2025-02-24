from django.contrib.auth import authenticate, logout, get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import UserProfileSerializer, ChangePasswordSerializer

User = get_user_model()


# Create a new user profile.
@csrf_exempt  # Use with extreme caution in production!
@api_view(['POST'])
def create_user_profile(request):
    if request.method == 'POST':
        serializer = UserProfileSerializer(data=request.data)

        if serializer.is_valid():
            # Save the new user profile and return success response
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login a user and get a JWT token using email and password.
@csrf_exempt  # Use with extreme caution in production!
@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        

# Logout the user by blacklisting the refresh token.
@csrf_exempt  # Use with extreme caution in production!
@api_view(['POST'])
def user_logout(request):
    if request.method == 'POST':
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the refresh token to prevent future usage
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print(e)
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


# Update the user's profile information.
@csrf_exempt  # Use with extreme caution in production!
@api_view(['POST'])
def update_user_profile(request):
    if request.method == 'POST':
        user = request.user   # Get the current user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# Delete the user's profile.
@csrf_exempt  # Use with extreme caution in production!
@api_view(['DELETE'])
def delete_user_profile(request):
    if request.method == 'DELETE':
        user = request.user
        user.delete()   # Delete the user profile
        return Response({"detail": "User profile deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


# Change the user's password.
@csrf_exempt  # Use with extreme caution in production!
@api_view(['POST'])
def change_user_password(request):
    if request.method == 'POST':
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.validated_data['old_password']):
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)