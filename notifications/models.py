from django.db import models
from django.utils import timezone
from django.conf import settings


class Notification(models.Model):
    NOTIFICATION_STATUS_CHOICES = [('new', 'New'), ('read', 'Read')]

    NOTIFICATION_TYPE_CHOICES = [('matchup', 'Matchup'), ('chat', 'Chat')]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications_received')
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='notifications_sent')
    detail = models.TextField()
    status = models.CharField(max_length=10, choices=NOTIFICATION_STATUS_CHOICES, default='new')
    type = models.CharField(max_length=10, choices=NOTIFICATION_TYPE_CHOICES, default='matchup')
    created_at = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.detail
        