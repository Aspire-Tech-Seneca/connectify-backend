from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    person_name = models.CharField(max_length=100)
    comment = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 star rating
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.person_name} - {self.rating} stars"


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
    

class Gallery(models.Model):

    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='gallery')

    def __str__(self):
        return f"{self.user.username} Gallery"


class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='gallery_images')
    image_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.image_url
    

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


class Matchup(models.Model):
    status_choices = [
        ('0', 'No status / not-started'),
        ('1', 'Matchup request sent'),
        ('2', 'Matchup request received'),
        ('3', 'Matchup request accepted. The two users are friends'),
        ('4', 'Request denied'),
        ('5', 'Request blocked, and the status of both sides are blocked, and they cannot send requests to each other'),
    ]

    requester = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='matchup_requests')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='matchup_received')
    status = models.CharField(max_length=10, choices=status_choices, default='0')

    class Meta:
        unique_together = ('requester', 'receiver')  # Prevent duplicate status pairs

    def __str__(self):
        return f"{self.requester} -> {self.receiver}: {self.status}"
