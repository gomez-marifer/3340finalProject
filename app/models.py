from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null= True)
    phone = models.CharField(max_length=200, null= True)
    email = models.CharField(max_length=200, null= True)
    date_created = models.DateTimeField(auto_now_add=True, null= True)
    
    def __str__(self):
        return self.name
    
class Assignment(models.Model):
    STATUS = (
        ('Assigned', 'Assigned'),
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Unable to Complete', 'Unable to Complete'),
    )

    customer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS, default='Assigned')
    due_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title
