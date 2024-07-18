from django.urls import path, include
from . import views

urlpatterns = [
    path('registerUser/',views.RegisterUserView.as_view(), name='registerUser'),
    path('registerSupplier/',views.RegisterSupplierView.as_view(), name='registerSupplier'),

    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('myAccount/', views.MyAccountView.as_view(), name='myAccount'),
    path('customerDashboard/', views.CustomerDashboardView.as_view(), name='customerDashboard'),
    path('supplierDashboard/', views.supplierDashboard, name='supplierDashboard'),

    path('activate/<uidb64>/<token>/', views.ActivateAccountView.as_view(), name='activate'),

    path('forgot_password/', views.ForgotPassword.as_view(), name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.ResetPasswordValidateView.as_view(), name='reset_password_validate'),
    path('reset_password/', views.ResetPasswordView.as_view(), name='reset_password'),
     path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),

    path('supplier/', include('supplier.urls')),
    path('customer/', include('customers.urls')),


]