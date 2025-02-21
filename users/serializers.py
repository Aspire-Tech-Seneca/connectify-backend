from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) # Ensure the password is write-only

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 
                  'email', 'password', ]
                #   'profile_picture', 'date_of_birth', 'location', 
                #   'language_prefer', 'gender', 'date_joined', 
                #   'interests', 'last_login',]

    def create(self, validated_data):
        """
        Create a new user instance, with the provided password being
        set to the user.
        """
        user = User.objects.create_user(
            # username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            # first_name=validated_data.get('first_name', ''),
            # last_name=validated_data.get('last_name', ''),
            # validated_data['date_of_birth'],
            # validated_data['location'],
            # validated_data['profile_picture'],
            # validated_data['language_prefer'],
            # validated_data['gender'],
            # validated_data['date_joined'],
            # validated_data['interests'],
            # validated_data['last_login'],
        )
        return user

