from mongoengine import Document, fields
from django.db import models
import bcrypt

class User(Document):
    fullName = fields.StringField(required=True, max_length=100)
    email = fields.EmailField(required=True, unique=True)
    age = fields.IntField(required=True)
    password = fields.StringField(required=True, max_length=100)

    meta = {
        'collection': 'users',  # MongoDB collection name
    }

    def set_password(self, password):
        # Hash the password before saving
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password):
        # Verify the hashed password
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
