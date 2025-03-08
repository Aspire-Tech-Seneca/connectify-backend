from django.conf import settings

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=255)
    age = models.IntegerField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    interest = models.ForeignKey('Interest', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')

    def save(self, *args, **kwargs):
        # Ensure the email is in lowercase
        self.email = self.email.lower()
        self.username = self.email
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.email


class ProfileImage(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='profile_image')
    image_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile Image'
    

class Interest(models.Model):
    interest_choices = (
        ('sports', 'Sports'),
        ('music', 'Music'),
        ('tech', 'Technology'),
        ('art', 'Art'),
        ('travel', 'Travel'),
    )

    name = models.CharField(max_length=100, choices=interest_choices, null=False, blank=True)

    def __str__(self):
        return self.name if self.name else "No Interest"
