from rest_framework import serializers
from events.models import Event
from django.contrib.auth import get_user_model


User = get_user_model()

class EventSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')  

    class Meta:
        model = Event
        fields = ['id', 'event_name', 'event_date', 'event_time', 'location', 
                  'description', 'category', 'event_image', 'created_by']
        