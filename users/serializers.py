from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from users.models import Interest, ProfileImage


User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, min_length=6)

    class Meta:
        model = User
        fields = ['email', 'fullname', 'age', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data.get('email'),  # Use email as username
            email = validated_data.get('email'),
            password = validated_data.get('password'),
            age = validated_data.get('age'),
            fullname = validated_data.get('fullname'),
        )
        user.set_password(validated_data['password'])  # Hash password
        user.save()
        return user


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = ['image_url']


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id', 'name']


class UserProfileSerializer(serializers.ModelSerializer):
    profile_image = ProfileImageSerializer(read_only=True)
    interest = InterestSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname', 'age', 'bio', 'location', 'profile_image', 'interest']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_new_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError({"confirm_new_password": "Passwords do not match."})
        return data
    

