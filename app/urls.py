from django.urls import path, include
from . import views

urlpatterns = [
<<<<<<< HEAD
    path('', views.home, name='home'),
    path('login/',views.loginPage, name = 'login'),
    path('register/',views.registerPage, name = 'register')
=======
    #path('admin/', admin.site.urls),
    path('',views.home, name = 'home'),
    path('login/',views.login, name = 'login'),
    path('register/',views.register, name = 'register'),
    path('aboutUs/',views.aboutUs, name = 'aboutUs'),
    path('tasks/',views.tasks, name = 'tasks'),
    path('administrator/',views.administrator, name = 'administrator')
>>>>>>> 2e57ce8a21565f8ea13c91f3e1b158aa14c632e7
]
