# members/api_views.py

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError

@csrf_exempt
@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return JsonResponse({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@csrf_exempt
@api_view(['POST'])
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return JsonResponse({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@csrf_exempt
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return JsonResponse({"error": "Username and password are required."}, status=400)
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return JsonResponse({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })
    else:
        return JsonResponse({"error": "Invalid credentials or user does not exist."}, status=400)
    
@csrf_exempt
@api_view(['POST'])
def register_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    try:
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=400)
        
        user = User.objects.create_user(username=username, password=password)
        return JsonResponse({"message": "User registered successfully"}, status=201)
    except IntegrityError:
        return Response({"error": "An error occurred. Username might already exist."}, status=400)