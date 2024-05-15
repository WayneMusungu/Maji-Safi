from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.myAccount ),
    path('registerUser/',views.RegisterUserView.as_view(), name='registerUser'),
    path('registerSupplier/',views.RegisterSupplierView.as_view(), name='registerSupplier'),

     path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('myAccount/', views.MyAccountView.as_view(), name='myAccount'),
    
    path('customerDashboard/', views.customerDashboard, name='customerDashboard'),
    path('supplierDashboard/', views.supplierDashboard, name='supplierDashboard'),

    path('activate/<uidb64>/<token>/', views.ActivateAccountView.as_view(), name='activate'),

    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),

    path('supplier/', include('supplier.urls')),
    path('customer/', include('customers.urls')),


]