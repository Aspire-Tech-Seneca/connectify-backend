import os
import sys

import environ

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()


# Add the project root to the Python path so you can import your models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # Adjust as needed
import mongoengine
from users.models import UserProfile

def run_migration():
    MONGODB_URI = env('MONGODB_URI')
    mongoengine.connect(db='MatchingUpDB', host=MONGODB_URI, alias='default')  # Connect to your database

    for user in UserProfile.objects():
        if not hasattr(user, 'fullname'): # or not hasattr(user, 'username'):
            user.fullname = "Default Name"
            # user.username = "default_user"
            user.age = 25
            # ... set other fields ...
            user.save()

    print("Migration 0002: Populating data completed.")

if __name__ == '__main__':
    run_migration()