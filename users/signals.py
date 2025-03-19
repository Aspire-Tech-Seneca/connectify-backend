from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import UserProfile, ProfileImage, Gallery

@receiver(post_save, sender=UserProfile)
def create_profile_image(sender, instance, created, **kwargs):
    if created:
        # When a new UserProfile is created, create a ProfileImage associated with it
        ProfileImage.objects.create(user=instance)


@receiver(post_save, sender=UserProfile)
def create_gallery(sender, instance, created, **kwargs):
    if created:
        Gallery.objects.create(user=instance)