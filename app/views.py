from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .filters import *
from .decorators import unauthenticated_user, allowed_users, admin_only
from .forms import CreateUserForm, AssignmentForm


# CUSTOMER REGISTER
@unauthenticated_user
#Customer Registration 
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

#Admin Registration
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

def aboutUs(request):
    return render(request, 'aboutUs.html', {})

def dashboard(request):
    return render(request, 'dashboard.html', {})         

#Customer Home Page
@login_required(login_url='login')
@allowed_users(['customer'])
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

#Admin Home Page
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

@login_required(login_url='login')
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

@login_required(login_url='login')
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

@login_required(login_url='login')
@admin_only
def deleteAssignment(request, pk):

    assignment = Assignment.objects.get(id=pk)
    if request.method == "POST":
        assignment.delete()
        return redirect('/home')
    
    context = {'item': assignment}
    return render(request, 'delete.html', context)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('dashboard')