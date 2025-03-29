from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer
from users.models import UserProfile


class CreateNotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        requester_id = request.data.get('requester')
        type_value = request.data.get('type')

        try:
            requester_user = UserProfile.objects.get(id=requester_id)
        except UserProfile.DoesNotExist:
            return Response({"error": "Requester not found."}, status=status.HTTP_404_NOT_FOUND)

        # Create the detail message with a default type value
        if not type_value:
            detail = f"{requester_user.fullname} sent you a matchup request"
        else:
            detail = f"{requester_user.fullname} sent you a {type_value} request"

        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            # Pass user instance, not ID
            notification = serializer.save(owner=user, detail=detail)

            response_data = {
                "id": notification.id,
                "owner": user.fullname,
                "requester": requester_user.fullname,
                "detail": detail,
                "created_at": notification.created_at,
                "status": notification.status,
                "type": notification.type,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ListNotificationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        notification_status = request.query_params.get('status', 'new')  # Default to 'new' if not provided

        # Fetch all notifications where the user is the owner
        notifications = Notification.objects.filter(owner=user, status=notification_status).order_by('-created_at')

        response_data = []

        for notification in notifications:
            response_data.append({
                "id": notification.id,
                "owner": notification.owner.fullname,
                "requester": notification.requester.fullname,
                "detail": notification.detail,
                "created_at": notification.created_at,
                "status": notification.status,
                "type": notification.type,
            })

        return Response(response_data, status=status.HTTP_200_OK)
        

class UpdateNotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        notification_id = request.data.get("id")
        new_status = request.data.get("status")

        if not notification_id:
            return Response({"error": "Notification ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        if new_status not in ["new", "read"]:
            return Response({"error": "Invalid status. Must be 'new' or 'read'."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            notification = Notification.objects.get(id=notification_id, owner=request.user)
        except Notification.DoesNotExist:
            return Response({"error": "Notification not found."}, status=status.HTTP_404_NOT_FOUND)

        notification.status = new_status
        notification.save()

        return Response({
            "id": notification.id,
            "status": notification.status,
            "message": f"Notification status updated to '{new_status}'."
        }, status=status.HTTP_200_OK)