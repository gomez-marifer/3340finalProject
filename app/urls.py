from django.urls import path, include
from . import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('home/',views.home, name = 'home'),
    path('login/',views.loginPage, name = 'login'),
    path('register/',views.registerPage, name = 'register'),
    path('adminRegister/',views.adminRegisterPage, name = 'adminRegister'),
    path('aboutUs/',views.aboutUs, name = 'aboutUs'),
    path('tasks/',views.tasks, name = 'tasks'),
    path('administrator/',views.administrator, name = 'administrator'),
    path('logout/', views.logoutUser, name='logout'),
    path('user/', views.userPage, name='user-page'),
    path('', views.dashboard, name='dashboard'),

]
