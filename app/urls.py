from django.urls import path, include
from . import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('',views.home, name = 'home'),
    path('login/',views.loginPage, name = 'login'),
    path('register/',views.registerPage, name = 'register'),
    path('aboutUs/',views.aboutUs, name = 'aboutUs'),
    path('tasks/',views.tasks, name = 'tasks'),
    path('update_task/<int:pk>/', views.update_task_status, name='update_task_status'),
    path('administrator/',views.administrator, name = 'administrator'),
    path('logout/', views.logoutUser, name='logout'),

]
