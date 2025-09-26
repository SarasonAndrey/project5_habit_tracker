from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["POST"])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")

    User.objects.create_user(username=username, password=password)
    return Response({"message": "User created"}, status=status.HTTP_201_CREATED)
