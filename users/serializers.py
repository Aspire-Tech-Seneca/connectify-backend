from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['email', 'fullname', 'age', ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # When creating a new user, make sure we don't explicitly set the username
        email = validated_data.get('email')
        user = UserProfile.objects.create_user(
            username=email,  # Use email as username
            email=email,
            password=validated_data.get('password'),
            fullname=validated_data.get('fullname'),
            age=validated_data.get('age')
        )
        return user
    

    # Override default update method
    def update(self, instance, validated_data):
        # If a new username provided in the request data, use it as new username if it's unique
        # If not, use new email provided in the request data as new username
        # If neither in the request data, use the old username
        print("==========Debugging: In the update method============")
        print(f"Instance data: {instance}")
        print(f"Validated data: {validated_data}")
        # Update the fields of the instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            print(f"Setting {attr} to {value} for {instance}")
        instance.save()
        return instance