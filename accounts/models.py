from django.contrib.auth.hashers import make_password, check_password
import mongoengine as me
from datetime import datetime

class UserProfile(me.Document):
    email = me.StringField(required=True, unique=True)
    username = me.StringField(required=True, unique=True)
    password = me.StringField(required=True)  
    first_name = me.StringField(max_length=30)
    last_name = me.StringField(max_length=30)
    profile_picture = me.StringField()  # URL or path to the profile picture
    date_of_birth = me.DateTimeField()  # Date of birth

    def set_password(self, raw_password):
        '''Set the password to the hashed version of raw_password'''
        self.password = make_password(raw_password)

    def verify_password(self, raw_password):
        '''Verify the provided password against the stored hashed password'''
        if not self.password:
            return False
        return check_password(raw_password, self.password)

    # Match Criteria
    age = me.IntField()
    gender = me.StringField(choices=["male", "female", "non-binary", "other"])
    location = me.PointField()  # Geospatial indexing
    interests = me.ListField(me.StringField())  # List of hobbies or interests
    bio = me.StringField(max_length=500)
    
    # Match Preferences
    age_range = me.ListField(me.IntField(), default=[18, 99])  # Preferred age range
    preferred_genders = me.ListField(me.StringField(), default=["any"])  # Gender preferences
    language_prefer = me.StringField(default="english")  # Preferred language

    # User Interaction
    matched_users = me.ListField(me.ReferenceField('self'))  # List of connected friends
    pending_requests = me.ListField(me.ReferenceField('self'))  # Friend requests sent
    blocked_users = me.ListField(me.ReferenceField('self'))  # Blocked users

    last_active = me.DateTimeField(default=datetime.now)  # Last active timestamp

    meta = {
        'indexes': [
            'email',  # For quick authentication
            'username',
            ('age', 'location'),  # Compound index for fast age-location queries
            ('location', 'interests'),  # Compound index for nearby interest-based search
            {'fields': ['$interests'], 'default_language': 'english'},  # Text search index for interests
            {'fields': [('location', '2dsphere')]},  # Geospatial index
        ]
    }

    def __str__(self):
        return self.username





# from django.db import models

# class User(models.Model):
#     username = models.CharField(max_length=30, unique=True)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=128)
#     date_of_birth = models.DateField(null=True, blank=True)
#     location = models.CharField(max_length=100, blank=True)

#     def __str__(self):
#         return self.username
    
