from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from events.models import Event
from events.serializers import EventSerializer
from users.azure_utils import upload_image
import json
import uuid
from datetime import datetime


# Create a new event API.
class CreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        event_data  = request.FILES.get('event_data')    # 
        event_image = request.FILES.get('event_image')   # optional

        if not event_data:
            return Response({"error": "No data formated correctly"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            json_data = json.load(event_data)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON content"}, status=status.HTTP_400_BAD_REQUEST)      
        
        event_image_url = None
        if event_image:   # Handle optional image
            extension = event_image.name.split('.')[-1]
            folder = "event_images"
            filename = f"{uuid.uuid4()}.{extension}"
            event_image_url = upload_image(event_image, filename, folder)

        json_data['event_image'] = event_image_url
        event_serializer = EventSerializer(data=json_data, context={"request": request})
        if event_serializer.is_valid():
            event_serializer.save(created_by=request.user)
            return Response(event_serializer.data, status=status.HTTP_201_CREATED)
        return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# List all events API.
class ListView(APIView):
    def post(self, request):
        """Retrieve events filtered by location and date range"""

        # 🔹 Extract filters from request.data
        location = request.data.get('location')
        date_from_str = request.data.get('date_from')
        date_to_str = request.data.get('date_to')

        try:
            date_from = datetime.strptime(date_from_str, "%Y-%m-%d").date() if date_from_str else None
            date_to = datetime.strptime(date_to_str, "%Y-%m-%d").date() if date_to_str else None
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        # 🔹 Filter events
        events = Event.objects.all()

        if location:
            events = events.filter(location=location)

        if date_from and date_to:
            events = events.filter(event_date__gte=date_from, event_date__lte=date_to)

        # 🔹 Serialize and return events
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)