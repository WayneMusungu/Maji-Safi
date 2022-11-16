from django.urls import path
from . import views
from accounts import views as AccountViews

urlpatterns = [
    path('', AccountViews.supplierDashboard, name='supplier'),
    path('profile/', views.supplierProfile, name='supplierProfile'),
    path('services/', views.services ,name='services'),
    path('services/type/<int:pk>/', views.water_by_type ,name='water_by_type'),
    
    
    # SERVICES CRUD
    
    path('services/type/add/', views.add_type, name ='add_type')

]