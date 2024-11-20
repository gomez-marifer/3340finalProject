from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import CreateUserForm, TaskForm

# Register page
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, "Account was created for " + user)
                
                return redirect('login')

        context = {'form': form}
        return render(request, 'register.html', context)

# Login page
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
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

@login_required(login_url='login')
def home(request):
    context = {}
    return render(request, 'home.html', context)

# About Us page
def aboutUs(request):
    return render(request, 'aboutUs.html', {})

@login_required(login_url='login')
def tasks(request):
    return render(request, 'tasks.html', {})

# Administrator page
def administrator(request):
    return render(request, 'admin.html', {})

# Logout user
def logoutUser(request):
    logout(request)
    return redirect('login')

# CRUD views for Task model
# Create a new task
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form})

# List all tasks
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})

# View a single task
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'task_detail.html', {'task': task})

# Update a task
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form})

# Delete a task
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'task_confirm_delete.html', {'task': task})
