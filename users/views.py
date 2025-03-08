from django.contrib.auth import authenticate, get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import UserRegisterSerializer, UserProfileSerializer, ChangePasswordSerializer, InterestSerializer
from users.models import ProfileImage, Interest
from users.azure_utils import upload_profile_image
from rest_framework.views import APIView
import uuid


User = get_user_model()


# Register API
class RegisterView(APIView):
    def post(self, request):
        if request.data.get('password') != request.data.get('confirm_password'):
            return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Login API (JWT Token)
class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(username=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# Logout API
class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the refresh token to prevent future usage
            return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


# Retrieve User Info API
class RetrieveUserInfoView(APIView):
    
    def get(self, request):
        user = request.user

        # Optimize the query 
        user = User.objects.select_related('profile_image', 'interest').get(id=user.id)
        if not user:
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# User Profile Update API
class UpdateUserProfileView(APIView):
    def patch(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Delete API
class DeleteUserProfileView(APIView):
    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    

# Change Password API
class ChangePasswordView(APIView):
    def put(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Verify old password
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({"old_password": "Incorrect old password."}, status=status.HTTP_400_BAD_REQUEST)

            # Set new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Upload Profile Image API
class ProfileImageUploadView(APIView):
    def put(self, request, *args, **kwargs):
        # Retrieve the user’s profile
        user_id = request.user.id
        profile_image, created = ProfileImage.objects.get_or_create(user_id=user_id)
        
        # Get the uploaded file
        uploaded_file = request.FILES.get('profile_image')
        if not uploaded_file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Optionally generate a unique filename
        extension = uploaded_file.name.split('.')[-1]
        unique_filename = f"profile_images/{uuid.uuid4()}.{extension}"
        
        # Upload the file to Azure Blob Storage
        blob_url = upload_profile_image(uploaded_file, unique_filename)
        
        # Save the blob URL in the database
        profile_image.image_url = blob_url
        profile_image.save()
        
        return Response({"message": "Image uploaded successfully", "image_url": blob_url},
                        status=status.HTTP_200_OK)


# Retrieve Profile Image API
class ProfileImageRetrieveView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        try:
            profileImage = ProfileImage.objects.get(user_id=user_id)
        except ProfileImage.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"image_url": profileImage.image_url}, status=status.HTTP_200_OK)


# Get Interest Choices API
class InterestListView(APIView):
    def get(self, request, *args, **kwargs):
        interest_choices = Interest.interest_choices
        # Retrieve choices from the Interest model
        interest_list = [{'value': value, 'label': label} for value, label in interest_choices]
        return Response(interest_list, status=status.HTTP_200_OK)
    

# Update User Interest API
class UserInterestSetView(APIView):
    def post(self, request, *args, **kwargs):
        # Get the user profile instance
        user = request.user  # Assuming the user is authenticated and has a UserProfile
        # Get the interest name from the request data
        interest_name = request.data.get('interest')
        
        # Validate the interest
        if interest_name not in dict(Interest.interest_choices).keys():
            return Response({'error': 'Invalid interest'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create or update the Interest instance
        interest, created = Interest.objects.get_or_create(name=interest_name)
        # Assign the interest to the user
        user.interest = interest
        user.save()
        
        # Serialize the response
        serializer = InterestSerializer(user.interest)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


# Retrieve User Interest API
class UserInterestRetrieveView(APIView):
    def get(self, request, *args, **kwargs):
        # Get the user profile instance
        user = request.user  # Assuming the user is authenticated and has a UserProfile
        # Check if the user has an interest assigned
        if not user.interest:
            return Response({'message': 'No interest selected'}, status=status.HTTP_200_OK)

        # Serialize the response
        serializer = InterestSerializer(user.interest)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Recommend Matchups (according to the user's interest) API
class RecommendMatchupsView(APIView):
    def post(self, request, *args, **kwargs):
        """Retrieve all users who have the same interest with the user."""
        user = request.user
        interest = user.interest

        if not interest:  # if the user hasn't selected an interest
            return Response({"message": "You have not selected an interest"}, status=status.HTTP_200_OK)

        # Fetch users who have this interest
        users = User.objects.filter(interest=interest).exclude(id=user.id).select_related('profile_image', 'interest')   

        if not users.exists():
            return Response({"message": "No other users share your interest"}, status=status.HTTP_200_OK)

        # Serialize user data
        serializer = UserProfileSerializer(users, many=True)  # `many=True` because it's a list
        return Response(serializer.data, status=status.HTTP_200_OK)