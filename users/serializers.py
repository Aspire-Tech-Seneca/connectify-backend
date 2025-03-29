from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from users.models import Interest, ProfileImage,Gallery, \
                         GalleryImage, Matchup, Review, UserProfile


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'email', 'fullname', 'location']
        # Note: username is the same as email in your model, so we don't need both

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'comment', 'rating', 'created_at']
        

#------------------------------------------------------------------------------------------
class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, min_length=6)

    class Meta:
        model = User
        fields = ['email', 'fullname', 'age', 'password', 'bio', 'location']

    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data.get('email'),  # Use email as username
            email = validated_data.get('email'),
            password = validated_data.get('password'),
            age = validated_data.get('age'),
            fullname = validated_data.get('fullname'),
            bio = validated_data.get('bio'),
            location = validated_data.get('location'),
        )
        user.set_password(validated_data['password'])  # Hash password
        user.save()
        return user


class ProfileImageSerializer(serializers.ModelSerializer):
    image_name = serializers.SerializerMethodField()

    class Meta:
        model = ProfileImage
        fields = ['image_name']

    def get_image_name(self, obj):
        if obj.image_url is None:
            return None
        
        return f"profile_image/{obj.image_url.split('/')[-1]}"


class GalleryImageSerializer(serializers.ModelSerializer):
    image_name = serializers.SerializerMethodField()

    class Meta:
        model = GalleryImage
        fields = ['image_name']

    def get_image_name(self, obj):
        if obj.image_url is None:
            return None

        return f"gallery_images/{obj.image_url.split('/')[-1]}"


class GallerySerializer(serializers.ModelSerializer):
    images = GalleryImageSerializer(many=True, read_only=True)  # Nested images

    class Meta:
        model = Gallery
        fields = ['images']


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id', 'name']


class UserProfileSerializer(serializers.ModelSerializer):
    profile_image = ProfileImageSerializer(read_only=True)
    gallery = GallerySerializer(read_only=True)
    interest = InterestSerializer(read_only=True)
    gallery_images = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname', 'age', 'bio', 'location', 
                  'profile_image', 'gallery', 'interest', 'gallery_images']

    def get_gallery_images(self, obj):
        gallery = getattr(obj, 'gallery', None)
        if gallery is not None:
            return [f"gallery_images/{image.image_url.split('/')[-1]}" for image in gallery.gallery_images.all()]
        return []    


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_new_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError({"confirm_new_password": "Passwords do not match."})
        return data
    

class MatchupSerializer(serializers.ModelSerializer):
    requester_id = serializers.IntegerField(source='requester.id', read_only=True)
    receiver_id = serializers.IntegerField(source='receiver.id', read_only=True)
    status = serializers.ChoiceField(choices=Matchup.status_choices)

    class Meta:
        model = Matchup
        fields = ['requester_id', 'receiver_id', 'status']


class MatchupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matchup
        fields = ['receiver', 'status']

    def validate_receiver(self, receiver):
        """Ensure the receiver exists and isn't the same as the requester."""
        requester = self.context['request'].user.userprofile
        if requester == receiver:
            raise serializers.ValidationError("You cannot send a matchup request to yourself.")
        if not User.objects.filter(id=receiver.id).exists():
            raise serializers.ValidationError("The user you're trying to send a request to does not exist.")
        return receiver


class MatchupUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matchup
        fields = ['status']

    def validate_status(self, status):
        """Validate the status transition based on the current status."""
        matchup = self.instance # get the matchup instance.
        current_status = matchup.status

        allowed_transitions = {
            Matchup.status_choices[1][0]: [Matchup.status_choices[3][0], Matchup.status_choices[4][0]], # 1: allow 3 or 4
            Matchup.status_choices[2][0]: [Matchup.status_choices[3][0], Matchup.status_choices[4][0]], # 2: allow 3 or 4
            Matchup.status_choices[0][0]: [Matchup.status_choices[1][0]], # 0: allow 1
            Matchup.status_choices[4][0]: [Matchup.status_choices[1][0]], # 4: allow 1 (allows a user who had a request denied to resend the request)
            Matchup.status_choices[1][0]: [Matchup.status_choices[5][0]], # 1: allow 5
            Matchup.status_choices[2][0]: [Matchup.status_choices[5][0]], # 2: allow 5
            Matchup.status_choices[3][0]: [Matchup.status_choices[5][0]], # 3: allow 5
        }

        if current_status not in allowed_transitions:
          raise serializers.ValidationError("This matchup status cannot be changed")

        if status not in allowed_transitions[current_status]:
            raise serializers.ValidationError(f"Invalid status transition from {current_status} to {status}")

        return status