from django.urls import path
from . import views
from accounts import views as AccountViews



urlpatterns = [
    path('', AccountViews.customerDashboard, name='customer'),
    path('profile/', views.customerProfile, name='customerProfile'),
    path('my_orders/', views.my_orders, name='customer_my_orders'),

]