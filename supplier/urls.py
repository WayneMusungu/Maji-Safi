from django.urls import path
from . import views
from accounts import views as AccountViews

urlpatterns = [
    path('', AccountViews.supplierDashboard, name='supplier'),
    path('profile/', views.supplierProfile, name='supplierProfile'),
    path('services/', views.services ,name='services'),
    path('services/category/<int:pk>/', views.water_by_category ,name='water_by_category'),

]