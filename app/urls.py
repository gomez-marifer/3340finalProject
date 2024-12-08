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
    path('update_task/<int:pk>/', views.update_task_status, name='update_task_status'),
    path('administrator/', views.manage_tasks, name='manage_tasks'),
    path('logout/', views.logoutUser, name='logout'),
    path('', views.dashboard, name='dashboard'),

    path('customers/', views.customer_list, name='customer_list'),
    path('customer/add/', views.create_customer, name='create_customer'),
    path('customer/edit/<int:pk>/', views.update_customer, name='update_customer'),
    path('customer/delete/<int:pk>/', views.delete_customer, name='delete_customer'),

    ###########################
    path('create_assignment/', views.createAssignment, name='create_assignment'),
    path('update_assignment/<str:pk>/', views.updateAssignment, name='update_assignment'),
    path('delete_assignment/<str:pk>/', views.deleteAssignment, name='delete_assignment'),
    path('user/', views.userPage, name='user-page'),

]
