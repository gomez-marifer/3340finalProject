from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('aboutUs/', views.aboutUs, name='aboutUs'),
    path('tasks/', views.tasks, name='tasks'),
    path('administrator/', views.administrator, name='administrator'),
    path('logout/', views.logoutUser, name='logout'),

    # Task CRUD views
    path('task_list/', views.task_list, name='task_list'),                     # List tasks
    path('task/<int:pk>/', views.task_detail, name='task_detail'),             # View a task
    path('task/new/', views.task_create, name='task_create'),                  # Create a task
    path('task/<int:pk>/edit/', views.task_update, name='task_update'),        # Edit a task
    path('task/<int:pk>/delete/', views.task_delete, name='task_delete'),      # Delete a task
]