from rest_framework import serializers
from accounts.models import User
from datetime import date


class UserSerializer(serializers.HyperlinkedModelSerializer):
    age = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['url', 'username', 'first_name', 'last_name', 
                  'email', 'password', 'age',]
                #   'profile_picture', 'date_of_birth',
                #   'location', 'language_prefer', 'gender', 'date_joined', 
                #   'interests', 'last_login',]

    def get_age(self, obj):
        """
        Calculate the age of the user from their birthdate.
        The `obj` parameter is the instance of the User model being serialized.
        """
        return int((date.today() - obj.date_of_birth).days / 365.25) 


