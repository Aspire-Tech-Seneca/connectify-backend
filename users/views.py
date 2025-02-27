from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import UserRegisterSerializer, UserProfileSerializer, ChangePasswordSerializer
from users.models import ProfileImage
from users.azure_utils import upload_profile_image
from rest_framework.views import APIView
import uuid


# Register API
class RegisterView(APIView):
    def post(self, request):
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


# User Profile Update API
class UpdateUserProfileView(APIView):
    def post(self, request):
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


class ProfileImageUploadView(APIView):
    def put(self, request, *args, **kwargs):
        # Retrieve the user’s profile
        user_id = request.user.id
        try:
            profile_image = ProfileImage.objects.get(user_id=user_id)
        except ProfileImage.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
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


class ProfileImageRetrieveView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        try:
            profileImage = ProfileImage.objects.get(user_id=user_id)
        except ProfileImage.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"image_url": profileImage.image_url}, status=status.HTTP_200_OK)
