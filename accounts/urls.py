from django.urls import path
from . import views

urlpatterns = [
    path('registerUser/',views.registerUser, name='registerUser'),
    path('registerSupplier/',views.registerSupplier, name='registerSupplier'),
    
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('myAccount', views.myAccount, name='myAccount'),
    path('customerDashboard/', views.customerDashboard, name='customerDashboard'),
    path('supplierDashboard/', views.supplierDashboard, name='supplierDashboard'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

]