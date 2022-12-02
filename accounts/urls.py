from django.urls import path
from . import views

urlpatterns = [
    path('registerUser/',views.registerUser, name='registerUser'),
    path('registerSupplier/',views.registerSupplier, name='registerSupplier'),
    
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard')

]