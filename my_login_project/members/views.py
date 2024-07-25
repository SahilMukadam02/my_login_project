# members/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def home(request):
    return render(request, 'home.html')

@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username=username, password=password)
        return render(request, 'thankyou.html')
    return render(request, 'register.html')

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'welcome.html', {'username': username})
    return render(request, 'login.html')
