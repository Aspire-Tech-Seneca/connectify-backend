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
    # username, password, first_name, last_name are already included in AbstractUser
    email = models.EmailField(unique=True)  # Make sure email is unique
    username = models.CharField(max_length=150, blank=True, null=True) # Optional; email will be used if not specified
    fullname = models.CharField(max_length=255, blank=True, null=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    # profile_image = models.ImageField(upload_to='profile_images/', blank=True, default="")
    
    USERNAME_FIELD = 'email'  # Use email as the unique identifier for authentication
    REQUIRED_FIELDS = []  

    # Adding related_name for groups and user_permissions to avoid "reverse accessor clash" issues
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='userprofile_set',  # Avoid clash with auth.User
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='userprofile_set',  # Avoid clash with auth.User
        blank=True
    )

    def __str__(self):
        return self.username if self.username else self.email
