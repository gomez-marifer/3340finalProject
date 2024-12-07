from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import CreateUserForm, TaskForm, CustomerForm
from .decorators import *

# User Authentication Views
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                group = Group.objects.get(name='user')
                user.groups.add(group)
                messages.success(request, "Account was created for " + user.username)
                return redirect('login')

        context = {'form': form}
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
def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    context = {}
    return render(request, 'home.html', context)


# Task Views
@login_required(login_url='login')
def tasks(request):
    user_tasks = Task.objects.filter(user=request.user)
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('tasks')

    context = {'tasks': user_tasks, 'form': form}
    return render(request, 'tasks.html', context)

@login_required(login_url='login')
def update_task_status(request, pk):
    task = Task.objects.get(id=pk)

    if task.user != request.user:
        return HttpResponse("Unauthorized", status=403)

    if request.method == 'POST':
        task.status = request.POST.get('status')
        task.save()
        return redirect('tasks')

    return render(request, 'update_task.html', {'task': task})


# Customer Views
@login_required(login_url='login')
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customer_list.html', {'customers': customers})

@login_required(login_url='login')
def create_customer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'form.html', {'form': form, 'title': 'Add Customer'})

@login_required(login_url='login')
def update_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'form.html', {'form': form, 'title': 'Edit Customer'})

@login_required(login_url='login')
def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        customer.delete()
        return redirect('customer_list')
    return render(request, 'confirm_delete.html', {'object': customer, 'title': 'Delete Customer'})


@admin_only
def manage_tasks(request):
    query = request.GET.get('q', '')
    tasks = Task.objects.filter(
        Q(title__icontains=query) | Q(user__username__icontains=query)
    ) if query else Task.objects.all()

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST.get('description', '')
        user_id = request.POST['user']
        user = User.objects.get(id=user_id)
        Task.objects.create(title=title, description=description, user=user)
        return redirect('manage_tasks')

    users = User.objects.all()
    return render(request, 'admin.html', {'tasks': tasks, 'users': users, 'query': query})


def aboutUs(request):
    return render(request, 'aboutUs.html', {})