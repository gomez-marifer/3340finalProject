from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate,login, logout

from django.contrib import messages

from .models import *
from .forms import CreateUserForm

# Create your views here.
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, "Account was created for " + user)
            
            return redirect('login')

    context = {'form':form}
    return render(request, 'register.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR Password is Incorrect')        
    context = {}
    return render(request, 'login.html', context)

def home(request):
<<<<<<< HEAD
    context = {}
    return render(request, 'home.html', context)
=======
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
>>>>>>> 2e57ce8a21565f8ea13c91f3e1b158aa14c632e7
