from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = User.objects.create_user(username=username, password=password)
    return Response({'message': 'User created'}, status=status.HTTP_201_CREATED)