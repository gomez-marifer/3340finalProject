from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('aboutUs/',views.aboutUs, name = 'aboutUs'),
    path('home/',views.home, name = 'home'),
    path('register/',views.registerPage, name = 'register'),
    path('adminRegister/',views.adminRegisterPage, name = 'adminRegister'),
    path('login/',views.loginPage, name = 'login'),   
    path('tasks/',views.tasks, name = 'tasks'),   
    path('create_assignment/', views.createAssignment, name='create_assignment'),
    path('update_assignment/<str:pk>/', views.updateAssignment, name='update_assignment'),
    path('delete_assignment/<str:pk>/', views.deleteAssignment, name='delete_assignment'),
    path('logout/', views.logoutUser, name='logout'),
]
