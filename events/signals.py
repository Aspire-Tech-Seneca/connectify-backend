from django.db.models.signals import post_save
from django.dispatch import receiver
from events.models import Event

@receiver(post_save, sender=Event)
def create_event_image(sender, instance, created, **kwargs):
    if created:
        # When a new Event is created, create a EventImage associated with it
        instance.save()

