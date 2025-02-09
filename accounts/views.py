from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.serializers import UserSerializer

@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        # Initialize the serializer with the data received in the request
        serializer = UserSerializer(data=request.data)

        # Validate the data
        if serializer.is_valid():
            # Save the data to the database
            serializer.save()
            return Response({
                'message': 'User created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    