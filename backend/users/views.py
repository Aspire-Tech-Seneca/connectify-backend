from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import jwt  # Import PyJWT
from django.conf import settings  # Import settings
import datetime
from .models import User
import json

@api_view(['POST'])
def create_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            full_name = data.get('fullName')
            email = data.get('email')
            age = data.get('age')
            password = data.get('password')

            if not full_name or not email or not password or age is None:
                return JsonResponse({"error": "Missing required fields"}, status=400)

            # Check if the user already exists
            if User.objects(email=email).first():
                return JsonResponse({"error": "User already exists"}, status=400)

            # Create user using MongoEngine model
            user = User(fullName=full_name, email=email, age=age)
            user.set_password(password)  # Hash password
            user.save()

            return JsonResponse({"message": "User created successfully!", "id": str(user.id)}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

def get_all_users(request):
    if request.method == 'GET':
        users = User.objects.all()
        users_list = [{
            "id": str(user.id),
            "fullName": user.fullName,
            "email": user.email,
            "age": user.age
        } for user in users]

        return JsonResponse({"users": users_list}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return JsonResponse({"error": "Missing email or password"}, status=400)

            # Find user by email
            user = User.objects(email=email).first()
            if not user:
                return JsonResponse({"error": "User not found"}, status=404)

            # Verify password
            if user.verify_password(password):
                # Generate JWT token
                payload = {
                    "user_id": str(user.id),
                    "email": user.email,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2),  # Token expiry
                }
                token = jwt.encode(payload, algorithm="HS256")

                return JsonResponse({
                    "message": "Login successful!",
                    "token": token,
                    "user": {
                        "id": str(user.id),
                        "fullName": user.fullName,
                        "email": user.email,
                        "age": user.age,
                    }
                })

            else:
                return JsonResponse({"error": "Invalid password"}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=400)