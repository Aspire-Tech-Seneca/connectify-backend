import os
import sys

import environ

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()


# Add the project root to the Python path so you can import your models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # Adjust as needed

import mongoengine
from users.models import UserProfile  # Import your Mongoengine models

def run_migration():
    MONGODB_URI = env('MONGODB_URI')
    mongoengine.connect(db='MatchingUpDB', host=MONGODB_URI, alias='default')  # Connect to your database

    # Add the new field to the model definition (if needed for subsequent migrations)
    # This might not be necessary if the field is already in your models.py
    # UserProfile._fields['new_field'] = mongoengine.StringField()  # Example

    print("Migration 0001: Adding new field completed.")

if __name__ == '__main__':
    run_migration()