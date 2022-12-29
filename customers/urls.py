from django.urls import path
from . import views
from accounts import views as AccountViews



urlpatterns = [
    path('', AccountViews.customerDashboard, name='customer'),
    path('profile/', views.customerProfile, name='customerProfile'),

]