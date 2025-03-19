from django.db import models
from django.conf import settings


class Event(models.Model):
    event_name = models.CharField(max_length=255)
    event_date = models.DateField(default=None, null=False, blank=False)
    event_time = models.TimeField(default=None, null=False, blank=False)
    location = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    # category = models.ForeignKey('EventCategory', on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    category = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="events_created")

    event_image = models.URLField(max_length=300, null=True, blank=True)  # Optional Image

    def __str__(self):
        return self.event_name
        

# class EventCategory(models.Model):
    # CATEGORY_CHOICES = [
    #     ("conference", "Conference"),
    #     ("workshop", "Workshop"),
    #     ("meetup", "Meetup"),
    #     ("other", "Other"),
    # ]

    # category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, null=True, blank=True)

#     def __str__(self):
#         return self.name if self.name else "No Category"


# class EventImage(models.Model):
#     event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='event_image')
#     image_url = models.URLField(max_length=500, blank=True, null=True)

#     def __str__(self):
#         return f'{self.event.event_name} Event Image'
