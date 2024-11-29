#from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Task


#from .models import Order

#class OrderForm(ModelForm):
 #   class Meta:
  #      model = Order
   #     fields = '__all__'

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status']  # User is excluded as it's auto-set in views