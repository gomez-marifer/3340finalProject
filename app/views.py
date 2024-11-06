from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
# Create your views here.
def home(request):
    return render(request, 'home.html',{})

def login(request):
    return render(request, 'login.html',{})

def register(request):
    return render(request, 'register.html',{})

def aboutUs(request):
    return render(request, 'aboutUs.html',{})

def tasks(request):
    return render(request, 'tasks.html',{})

def administrator(request):
    return render(request, 'admin.html',{})