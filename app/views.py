from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import *
from .decorators import *
from .filters import *
from .decorators import unauthenticated_user, allowed_users, admin_only
from .forms import CreateUserForm, TaskForm, AssignmentForm


# CUSTOMER REGISTER
@unauthenticated_user
# User Authentication Views
def registerPage(request):

    form = CreateUserForm()
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

    form = CreateUserForm()
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


#@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin'])
#def administrator(request):
 #   return render(request, 'admin.html',{})

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('dashboard')

# Task Views
@login_required(login_url='login')
def tasks(request):
    user_assignment = Assignment.objects.filter(customer=request.user)
    form = AssignmentForm()

    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.user = request.customer
            assignment.save()
            return redirect('tasks')
    
    total_assignments = user_assignment.count()

    pending = user_assignment.filter(status='Pending').count()
    completed = user_assignment.filter(status='Completed').count()
    

    context = {'assignments': user_assignment, 'form': form, 'total_assignments':total_assignments, 'pending': pending, 'completed': completed}
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

def dashboard(request):
    return render(request, 'dashboard.html', {})


##################################

@login_required(login_url='login')
@admin_only
def home(request):
    assignments = Assignment.objects.all()

    total_assignments = assignments.count()

    pending = assignments.filter(status='Pending').count()
    completed = assignments.filter(status='Completed').count()
    
    myFilter = AssignmentFilter(request.GET, queryset=assignments)
    assignments = myFilter.qs

    context = {'assignments':assignments, 'total_assignments': total_assignments, 'pending': pending, 'completed': completed, 'myFilter': myFilter}
    return render(request, 'home.html', context)

def createAssignment(request):

    form = AssignmentForm()
    if request.method == 'POST':
        #print('Printing POST:', request.POST)
        form = AssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/home')

    context={'form':form}
    return render(request, 'assignment_form.html', context)

def updateAssignment(request, pk):

    assignment = Assignment.objects.get(id=pk)
    form = AssignmentForm(instance=assignment)
    
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect('/home')

    context = {'form': form}
    return render(request, 'assignment_form.html', context)

def deleteAssignment(request, pk):

    assignment = Assignment.objects.get(id=pk)
    if request.method == "POST":
        assignment.delete()
        return redirect('/home')
    
    context = {'item': assignment}
    return render(request, 'delete.html', context)

def userPage(request):
    assignments = Assignment.objects.all()

    myFilter = AssignmentFilter(request.GET, queryset=assignments)
    assignments = myFilter.qs

    context = {'assignments': assignments, 'myFilter': myFilter}
    return render(request, 'user.html', context)