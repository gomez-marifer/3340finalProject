from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=200, null= True)
    phone = models.CharField(max_length=200, null= True)
    email = models.CharField(max_length=200, null= True)
    date_created = models.DateTimeField(auto_now_add=True, null= True)

    def __str__(self):
        return self.name
    

#New class
class Task (models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title