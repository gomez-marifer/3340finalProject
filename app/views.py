from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.models import Group

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from .models import *
from .forms import CreateUserForm,TaskForm
from .decorators import *

# Create your views here.
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
                group = Group.objects.get(name='user')
                user.groups.add(group)
                messages.success(request, "Account was created for " + user)
                
                return redirect('login')

        context = {'form':form}
        return render(request, 'register.html', context)


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

def aboutUs(request):
    return render(request, 'aboutUs.html',{})

@login_required(login_url='login')
def tasks(request):
    user_tasks = Task.objects.filter(user=request.user)  # Fetch tasks for the logged-in user
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Assign the logged-in user to the task
            task.save()
            return redirect('tasks')

    context = {'tasks': user_tasks, 'form': form}
    return render(request, 'tasks.html', context)

@login_required(login_url='login')
def update_task_status(request, pk):
    task = Task.objects.get(id=pk)

    # Ensure only the owner can update the task
    if task.user != request.user:
        return HttpResponse("Unauthorized", status=403)

    if request.method == 'POST':
        task.status = request.POST.get('status')
        task.save()
        return redirect('tasks')

    return render(request, 'update_task.html', {'task': task})


@admin_only
def administrator(request):
    return render(request, 'admin.html',{})

def logoutUser(request):
    logout(request)
    return redirect('login')

