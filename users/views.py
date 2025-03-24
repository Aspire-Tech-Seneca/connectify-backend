from django.contrib.auth import authenticate, get_user_model
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import UserRegisterSerializer, UserProfileSerializer, \
                              ChangePasswordSerializer, InterestSerializer, ProfileImageSerializer, \
                              GallerySerializer, MatchupSerializer
from users.models import ProfileImage, Interest, Matchup, Gallery, GalleryImage
from users.azure_utils import upload_image, delete_image
from notifications.models import Notification
from rest_framework.views import APIView
from django.db.models import Q
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

        if not user:
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Optimize the query 
        user = User.objects.select_related('profile_image', 'gallery', 'interest')\
                        .prefetch_related('gallery__gallery_images')\
                        .get(id=user.id)

        # Safely extract gallery images if gallery exists
        gallery_images = []
        if hasattr(user, 'gallery') and user.gallery:
            gallery_images = [
                'gallery_images/' + image.image_url.split('/')[-1]
                for image in user.gallery.gallery_images.all()
            ]
                    
        serializer = UserProfileSerializer(user)
        data = serializer.data
        data['gallery_images'] = gallery_images

        return Response(data, status=status.HTTP_200_OK)


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
        profileimage_name = user.profile_image.image_url.split('/')[-1]
        if not profileimage_name:
            delete_image(profileimage_name)
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


# Upload Gallery Image API -- For profile image and gallery images
class ProfileImageUploadView(APIView):
    """
    API endpoint to upload one gallery image for the authenticated user.
    """

    def put(self, request, *args, **kwargs):
        # Retrieve the user’s profile
        user_id = request.user.id
        profile_image, created = ProfileImage.objects.get_or_create(user_id=user_id)
        
        # Get the profile image file
        profileimage_file = request.FILES.get('profile_image')
        if not profileimage_file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate a unique filename
        extension = profileimage_file.name.split('.')[-1]
        folder = "profile_images"
        profileimage_filename = f"{uuid.uuid4()}.{extension}"
        
        # Upload the profileimage file to Azure Blob Storage with a unique filename
        blob_url = upload_image(profileimage_file, profileimage_filename, folder)
        
        # Save the profile image URL in the database
        profile_image.image_url = blob_url
        profile_image.save()

        # Get the list of gallery image files
        galleryimage_files = request.FILES.getlist('gallery_images')

        if galleryimage_files:
            gallery, created = Gallery.objects.get_or_create(user_id=user_id)
            folder = "gallery_images"

            for galleryimage_file in galleryimage_files:
                # Optionally generate a unique filename
                extension = galleryimage_file.name.split('.')[-1]
                galleryimage_filename = f"{uuid.uuid4()}.{extension}"
                
                # Upload the gallery image file to Azure Blob Storage with a unique filename
                blob_url = upload_image(galleryimage_file, galleryimage_filename, folder)
                
                # Save the gallery image URL in the database
                gallery_image = GalleryImage(gallery=gallery, image_url=blob_url)
                gallery_image.save()
            gallery.save()

        # Serialize the response
        
        return Response({"message": "Images uploaded successfully"},
                        status=status.HTTP_200_OK)


# Retrieve Profile Image API
class ProfileImageRetrieveView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user

        if not user:
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Optimize the query 
        user = User.objects.select_related('profile_image', 'gallery', 'interest')\
                        .prefetch_related('gallery__gallery_images')\
                        .get(id=user.id)
        
        profile_image = None
        if hasattr(user, 'profile_image') and user.profile_image and user.profile_image.image_url:
            image_name = user.profile_image.image_url.split('/')[-1]
            profile_image = f"profile_images/{image_name}"

        # Safely extract gallery images if gallery exists
        gallery_images = []
        if hasattr(user, 'gallery') and user.gallery:
            gallery_images = [
                'gallery_images/' + image.image_url.split('/')[-1]
                for image in user.gallery.gallery_images.all()
            ]

        return Response(
            {
                "profile_image": profile_image, 
                "gallery_images": gallery_images
            },
            status=status.HTTP_200_OK
        )


# Delete Gallery Image API
class GalleryImageDeleteView(APIView):
    def patch(self, request, *args, **kwargs):
        user = request.user
        if not user:
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Optimize the query 
        user = User.objects.select_related('profile_image', 'gallery', 'interest')\
                        .prefetch_related('gallery__gallery_images')\
                        .get(id=user.id)
        
        image = request.data.get('image')
        if not image:
            return Response({"error": "Image not provided"}, status=status.HTTP_400_BAD_REQUEST)

        if hasattr(user, 'gallery') and user.gallery:
            try:
                user.gallery.gallery_images.filter(image_url__contains=image).delete()
                delete_image(image.split('/')[-1], "gallery_images")
            except GalleryImage.DoesNotExist:
                return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Gallery not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Gallery images deleted successfully"}, status=status.HTTP_200_OK)


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

        # Fetch users who have an existing matchup with this user in restricted statuses
        excluded_users = Matchup.objects.filter(
            Q(requester=user, status__in=[1, 2, 3, 5]) | 
            Q(receiver=user, status__in=[1, 2, 3, 5])
        ).values_list('requester', 'receiver', flat=False)

        # Flatten the tuple results and remove the current user's ID
        excluded_user_ids = {uid for pair in excluded_users for uid in pair if uid != user.id}
        
        # Fetch users who have this interest excluding those in an active/blocked matchup
        users = User.objects.filter(interest=interest).exclude(id__in=excluded_user_ids).exclude(id=user.id).select_related('profile_image', 'interest')   

        if not users.exists():
            return Response({"message": "No other users share your interest"}, status=status.HTTP_200_OK)

        # Serialize user data
        serializer = UserProfileSerializer(users, many=True)  # `many=True` because it's a list
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class RequestMatchupAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        receiver_id = request.data.get('receiver-user-id')
        if not receiver_id:
            return Response({"detail": "receiver-user-id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            return Response({"detail": "Receiver user not found."}, status=status.HTTP_400_BAD_REQUEST)

        requester = request.user

        # Check if a matchup already exists for both users
        matchup_exists = Matchup.objects.filter(
            Q(requester=requester, receiver=receiver) | 
            Q(requester=receiver, receiver=requester)
        ).exists()

        if matchup_exists:
            # Retrieve both matchup records
            matchups = Matchup.objects.filter(
                Q(requester=requester, receiver=receiver) | 
                Q(requester=receiver, receiver=requester)
            )

            matchup_requester = matchups.get(requester=requester, receiver=receiver)
            matchup_receiver = matchups.get(requester=receiver, receiver=requester)

            if matchup_requester.status == Matchup.status_choices[5][0]:  # 'blocked'
                return Response({"message": "Request blocked. You cannot send requests to this user."}, status=status.HTTP_403_FORBIDDEN)

            elif matchup_receiver.status == Matchup.status_choices[5][0]:  # 'blocked'
                return Response({"message": "Request blocked. You cannot send requests to this user."}, status=status.HTTP_403_FORBIDDEN)

            elif matchup_requester.status == Matchup.status_choices[1][0]:  # 'sent'
                return Response({"message": "The matchup request has already been sent, please wait for confirmation."}, status=status.HTTP_200_OK)

            elif matchup_requester.status == Matchup.status_choices[2][0]:  # 'received'
                return Response({"message": "The user sent you a matchup request, please confirm it."}, status=status.HTTP_400_BAD_REQUEST)

            elif matchup_requester.status == Matchup.status_choices[3][0]:  # 'confirmed'
                return Response({"message": "You are already friends."}, status=status.HTTP_400_BAD_REQUEST)

            elif matchup_requester.status == Matchup.status_choices[4][0]:  # 'denied'
                matchup_requester.status = Matchup.status_choices[1][0]  # 'sent'
                matchup_receiver.status = Matchup.status_choices[2][0]  # 'received'
                matchup_receiver.save()
                matchup_requester.save()
                return Response({"message": "The matchup request has been sent successfully."}, status=status.HTTP_200_OK)

            else:
                return Response({"detail": "Matchup status is invalid"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            # Create mirrored matchup records
            Matchup.objects.bulk_create([
                Matchup(requester=requester, receiver=receiver, status=Matchup.status_choices[1][0]),  # 'sent'
                Matchup(requester=receiver, receiver=requester, status=Matchup.status_choices[2][0])   # 'received'
            ])

            # Create notification for the receiver
            Notification.objects.create(
                owner=receiver,
                requester=requester,
                detail=f"{requester.fullname} sent you a matchup request",
                status='new',
                type='matchup'
            )

            return Response({"message": "The matchup request has been sent successfully."}, status=status.HTTP_201_CREATED)


class GetMatchupStatusAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Using receiver as the logged-in user to check the status of the received requests
        # and to get the list of users (user_ids) who sent the requests
        receiver = request.user.id
        matchups = Matchup.objects.filter(requester=receiver, status=Matchup.status_choices[2][0])
        requesters = [matchup.receiver for matchup in matchups]
        serializer = UserProfileSerializer(requesters, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConfirmMatchupRequestAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        requester_id = request.data.get('requester-user-id')
        if not requester_id:
            return Response({"detail": "requester-user-id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            requester = User.objects.get(id=requester_id)
        except User.DoesNotExist:
            return Response({"detail": "Requester user not found."}, status=status.HTTP_400_BAD_REQUEST)

        receiver_id = request.user.id

        # Check if both matchup records exist in the "received" and "sent" state
        try:
            matchup_requester = Matchup.objects.get(requester=requester_id, receiver=receiver_id, status=Matchup.status_choices[1][0])  # 'received'
            matchup_receiver = Matchup.objects.get(requester=receiver_id, receiver=requester_id, status=Matchup.status_choices[2][0])  # 'sent'
        except Matchup.DoesNotExist:
            return Response({"detail": "Matchup request not found or invalid status."}, status=status.HTTP_400_BAD_REQUEST)

        # Update both records to 'confirmed'
        matchup_requester.status = Matchup.status_choices[3][0]  # 'confirmed'
        matchup_receiver.status = Matchup.status_choices[3][0]  # 'confirmed'
        matchup_requester.save()
        matchup_receiver.save()

        # Create notification for the receiver
        Notification.objects.create(
            owner=requester,  # The message will sent to the user who sent matchup request previously
            requester=request.user,
            detail=f"{request.user.fullname} confirmed you matchup request, now you can chat",
            status='new',
            type='matchup'
        )

        return Response({"message": "The matchup request has been confirmed successfully."}, status=status.HTTP_200_OK)


class GetMyMatchupListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        matchups_requester = Matchup.objects.filter(requester=user, status=Matchup.status_choices[3][0])
        matchups_receiver = Matchup.objects.filter(receiver=user, status=Matchup.status_choices[3][0])

        matchup_users_requester = [m.receiver for m in matchups_requester]
        matchup_users_receiver = [m.requester for m in matchups_receiver]

        matchup_users = list(set(matchup_users_requester + matchup_users_receiver))

        serializer = UserProfileSerializer(matchup_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class DenyMatchupRequestAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        requester_id = request.data.get('requester-user-id')
        if not requester_id:
            return Response({"detail": "requester-user-id is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            requester = User.objects.get(id=requester_id)
        except User.DoesNotExist:
            return Response({"detail": "Requester user not found."}, status=status.HTTP_400_BAD_REQUEST)

        receiver = request.user

        # Check if a matchup exists between the users
        try:
            matchup_requester = Matchup.objects.get(requester=requester, receiver=receiver, status=Matchup.status_choices[1][0])
            matchup_receiver = Matchup.objects.get(requester=receiver, receiver=requester, status=Matchup.status_choices[2][0])
        except Matchup.DoesNotExist:
            return Response({"detail": "Matchup request not found."}, status=status.HTTP_400_BAD_REQUEST)

        # Update both records to "blocked"
        matchup_requester.status = Matchup.status_choices[4][0]  # 'denied'
        matchup_receiver.status = Matchup.status_choices[4][0]  # 'denied'
        matchup_requester.save()
        matchup_receiver.save()

        # Create notification for the receiver
        Notification.objects.create(
            owner=requester,  # The message will sent to the user who sent matchup request previously
            requester=request.user,
            detail=f"{request.user.fullname} denied you matchup request, you can send them new requests later",
            status='new',
            type='matchup'
        )

        return Response({"message": "User has been denied successfully."}, status=status.HTTP_200_OK)
    

class BlockMatchupRequestAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        requester_id = request.data.get('requester-user-id')
        if not requester_id:
            return Response({"detail": "requester-user-id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            requester = User.objects.get(id=requester_id)
        except User.DoesNotExist:
            return Response({"detail": "Requester user not found."}, status=status.HTTP_400_BAD_REQUEST)

        receiver = request.user

        # Check if a matchup exists between the users
        try:
            matchup_requester = Matchup.objects.get(requester=requester, receiver=receiver, status=Matchup.status_choices[1][0])
            matchup_receiver = Matchup.objects.get(requester=receiver, receiver=requester, status=Matchup.status_choices[2][0])
        except Matchup.DoesNotExist:
            return Response({"detail": "Matchup request not found."}, status=status.HTTP_400_BAD_REQUEST)

        # Update both records to "blocked"
        matchup_requester.status = Matchup.status_choices[5][0]  # 'blocked'
        matchup_receiver.status = Matchup.status_choices[5][0]  # 'blocked'
        matchup_requester.save()
        matchup_receiver.save()

        # Create notification for the receiver
        Notification.objects.create(
            owner=requester,  # The message will sent to the user who sent matchup request previously
            requester=request.user,
            detail=f"{request.user.fullname} blocked you matchup request, you cannot send them any requests",
            status='new',
            type='matchup'
        )
        return Response({"message": "User has been blocked successfully."}, status=status.HTTP_200_OK)