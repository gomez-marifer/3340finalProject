from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate,login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import *
from .forms import CreateUserForm
from .decorators import unauthenticated_user, allowed_users, admin_only

# CUSTOMER REGISTER
@unauthenticated_user
def registerPage(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            messages.success(request, "Account was created for " + username)
            
            return redirect('login')

    context = {'form':form}
    return render(request, 'register.html', context)

# ADMIN
@unauthenticated_user
def adminRegisterPage(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            
            group = Group.objects.get(name='admin')
            user.groups.add(group)
            messages.success(request, "Account was created for " + username)
            
            return redirect('login')

    context = {'form':form}
    return render(request, 'adminRegister.html', context)

@unauthenticated_user
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

#only admins can access
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def administrator(request):
    return render(request, 'admin.html',{})

@login_required(login_url='login')
@admin_only
def home(request):
    context = {}
    return render(request, 'home.html', context)

#only customers can access
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def tasks(request):
    return render(request, 'tasks.html',{})

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    context = {}
    return render(request, 'user.html', context)

#no need to log in
def aboutUs(request):
    return render(request, 'aboutUs.html',{})

def logoutUser(request):
    logout(request)
    return redirect('login')

def dashboard(request):
    context = {}
    return render(request, 'dashboard.html', context)