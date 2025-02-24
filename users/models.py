from django.conf import settings

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserInterest(models.Model):
    interest_choices = [
        ('sports', 'Sports'),
        ('music', 'Music'),
        ('tech', 'Technology'),
        ('art', 'Art'),
        ('travel', 'Travel'),
        # Add other interests as needed
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    interest = models.CharField(max_length=100, choices=interest_choices, null=True, blank=True)

    def __str__(self):
        return f'{self.user} - {self.interest}'


class UserProfile(AbstractUser):
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=255)
    age = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Ensure the email is in lowercase
        self.email = self.email.lower()
        self.username = self.email
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.email
