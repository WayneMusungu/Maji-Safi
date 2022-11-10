from django.urls import path
from . import views
from accounts import views as AccountViews

urlpatterns = [
    path('', AccountViews.supplierDashboard, name='supplier'),
    path('profile/', views.supplierProfile, name='supplierProfile'),
]