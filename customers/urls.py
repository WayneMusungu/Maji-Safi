from django.urls import path
from accounts.views import CustomerDashboardView
from . import views

urlpatterns = [
    path('', CustomerDashboardView.as_view(), name='customer'),
    path('profile/', views.CustomerProfileView.as_view(), name='customerProfile'),
    path('my_orders/', views.my_orders, name='customer_my_orders'),
    path('order_detail/<int:order_number>/', views.order_detail, name='order_detail'),
]